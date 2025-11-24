from fsspec import filesystem, AbstractFileSystem
from typing import Any


GCS_PREFIX = 'gs://'
GCS_FILE_SYSTEM = 'gcs'
LOCAL_FILE_SYSTEM = 'file'


def choose_file_system(path: str) -> AbstractFileSystem:
	return filesystem(GCS_FILE_SYSTEM) if path.startswith(GCS_PREFIX) else filesystem(LOCAL_FILE_SYSTEM)


def open_file(path: str, mode: str = 'r') -> Any:
	file_system = choose_file_system(path)
	return file_system.open(path, mode)