import re
from pathlib import Path

from src.models.email import Email


class FileWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, data: str):
        path = Path(self.file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")


class EmailWriter:
    def __init__(self, output_directory: str):
        self.output_directory = Path(output_directory)

    def save(self, email: Email, source_name: str) -> Path:
        email_directory = self.output_directory / (Path(source_name).stem or "email")
        email_directory.mkdir(parents=True, exist_ok=True)

        if email.html_body is not None:
            FileWriter(str(email_directory / "email.html")).save(email.html_body)

        if email.attachments:
            attachment_directory = email_directory / "attachments"
            attachment_directory.mkdir(parents=True, exist_ok=True)
            used_names = set()

            for index, attachment in enumerate(email.attachments, start=1):
                filename = self._safe_filename(attachment.filename, index)
                path = Path(filename)
                base_name = path.stem
                suffix = path.suffix
                unique_name = filename
                duplicate_number = 2
                while unique_name.casefold() in used_names:
                    unique_name = f"{base_name}-{duplicate_number}{suffix}"
                    duplicate_number += 1
                used_names.add(unique_name.casefold())
                (attachment_directory / unique_name).write_bytes(attachment.payload)

        return email_directory

    @staticmethod
    def _safe_filename(filename: str, index: int) -> str:
        filename = Path(filename.replace("\\", "/")).name
        filename = re.sub(r'[<>:"|?*\x00-\x1f]', "_", filename).strip(" .")
        return filename or f"attachment-{index}.bin"