import uuid

from django.db.models import Model
from django.core.files import File


def create_uuid_filename(instance: Model, filename: str) -> str:
    _, ext = filename.rsplit(".", 1)

    return f"{uuid.uuid4()}.{ext}"


def chunked(file_to_chunk: File, chunk_size=512):
    with file_to_chunk.open() as f:
        while chunk := f.read(chunk_size):
            yield chunk
