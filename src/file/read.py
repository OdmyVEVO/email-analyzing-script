from collections.abc import Iterator


class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self) -> Iterator[str]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            yield from file

class DirectoryReader:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.files = None

    def list_files(self) -> list:
            import os
            if self.files is None:
                self.files = [f for f in os.listdir(self.directory_path) if os.path.isfile(os.path.join(self.directory_path, f))]
            return self.files