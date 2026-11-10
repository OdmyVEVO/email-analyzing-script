from collections.abc import Iterator
import os
from pathlib import Path

from src.models.file import File


SUPPORTED_FORMATS = ("eml",)


def is_supported_format(file: File) -> bool:
    return file.extension.lower() in SUPPORTED_FORMATS


class FileReader:
    def __init__(self, file: File):
        self.file = file

    def read_file(self) -> Iterator[str]:
        if not is_supported_format(self.file):
            print(f"Skipping file: {self.file.name}. Reason: unsupported extension.")
            return
        with open(self.file.path, 'r', encoding='utf-8') as source:
            yield from source

class DirectoryReader:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.files = None

    def list_files(self) -> list:
        if self.files is None:
            self.files = []
            for file_name in os.listdir(self.directory_path):
                file_path = Path(self.directory_path) / file_name
                if not file_path.is_file():
                    continue

                file = File(
                    name=file_name,
                    size=file_path.stat().st_size,
                    path=str(file_path),
                )
                if not is_supported_format(file):
                    print(f"Skipping file: {file.name}. Reason: unsupported extension.")
                    continue

                self.files.append(file)
        return self.files