"""Kepler addition: time-limited signed links for stored files.

Tool HTML embeds in the chat run in a sandboxed iframe without the user's session, so they cannot
fetch ``/api/v1/files/{id}/content``. This router serves a file when the URL carries a valid
HMAC signature (keyed with ``WEBUI_SECRET_KEY``) and an unexpired timestamp, so a tool can embed
media it saved into Open WebUI storage (e.g. the Seedance video tool's stitched clips).

Kept in its own module so upstream merges never touch it; wired up with one line in ``main.py``.
"""

import asyncio
import hashlib
import hmac
import logging
import time
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse

from open_webui.env import WEBUI_SECRET_KEY
from open_webui.models.files import Files
from open_webui.storage.provider import Storage
from open_webui.utils.auth import get_admin_user

log = logging.getLogger(__name__)

router = APIRouter()

DEFAULT_TTL_SECONDS = 30 * 24 * 3600


def _signature(file_id: str, expires_at: int) -> str:
    msg = f'kepler-file:{file_id}:{expires_at}'.encode()
    return hmac.new(WEBUI_SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()


def sign_file_url(file_id: str, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> str:
    """Return a relative URL that serves the file without a session until ``ttl_seconds`` from now."""
    expires_at = int(time.time()) + max(60, int(ttl_seconds))
    return f'/api/v1/files/{file_id}/signed?exp={expires_at}&sig={_signature(file_id, expires_at)}'


@router.get('/{id}/signed-url')
async def create_signed_file_url(
    id: str,
    ttl: int = Query(DEFAULT_TTL_SECONDS, ge=60, le=365 * 24 * 3600, description='Lifetime in seconds'),
    user=Depends(get_admin_user),
):
    """Admin helper: mint a signed link for an existing file (used for testing and integrations)."""
    file = await Files.get_file_by_id(id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return {'id': id, 'url': sign_file_url(id, ttl), 'expires_in': ttl}


@router.get('/{id}/signed')
async def get_signed_file_content(
    id: str,
    exp: int = Query(..., description='Unix expiry timestamp'),
    sig: str = Query(..., description='HMAC-SHA256 signature'),
):
    if exp < int(time.time()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Link expired')
    if not hmac.compare_digest(sig, _signature(id, exp)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid signature')

    file = await Files.get_file_by_id(id)
    if not file or not file.path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    try:
        file_path = Path(await asyncio.to_thread(Storage.get_file, file.path))
    except Exception as exc:
        log.exception('kepler_files: storage lookup failed for %s', id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from exc
    if not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    meta = file.meta or {}
    content_type = meta.get('content_type') or 'application/octet-stream'
    filename = quote(meta.get('name') or file.filename or id)
    headers = {
        'Content-Disposition': f"inline; filename*=UTF-8''{filename}",
        'Cache-Control': 'private, max-age=3600',
        'Accept-Ranges': 'bytes',
    }
    return FileResponse(file_path, headers=headers, media_type=content_type)
