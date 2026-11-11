from email import policy
from email.parser import BytesFeedParser
from mimetypes import guess_extension
from typing import Optional

from src.file.read import FileReader
from src.models.email import Email, EmailAttachment
from src.models.file import File


class FileParser:
    def __init__(self, file: File):
        self.file = file

    def parse(self) -> Optional[Email]:
        chunks = FileReader(self.file).read_file()
        if chunks is None:
            return None

        parser = BytesFeedParser(policy=policy.default)
        for chunk in chunks:
            parser.feed(chunk)
        message = parser.close()

        body_parts = []
        html_parts = []
        attachments = []

        for part in message.walk():
            if part.is_multipart():
                continue

            content_type = part.get_content_type()
            filename = part.get_filename()
            is_attachment = (
                part.get_content_disposition() == "attachment"
                or filename is not None
                or content_type not in ("text/plain", "text/html")
            )
            if is_attachment:
                payload = part.get_payload(decode=True) or b""
                extension = ".ics" if content_type == "text/calendar" else guess_extension(content_type)
                attachments.append(
                    EmailAttachment(
                        filename=filename or (
                            f"attachment-{len(attachments) + 1}"
                            f"{extension or '.bin'}"
                        ),
                        content_type=content_type,
                        payload=payload,
                    )
                )
                continue

            try:
                content = part.get_content()
            except (LookupError, UnicodeDecodeError):
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                try:
                    content = payload.decode(charset, errors="replace")
                except LookupError:
                    content = payload.decode("utf-8", errors="replace")

            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="replace")

            if content_type == "text/plain":
                body_parts.append(content)
            else:
                html_parts.append(content)

        html_body = "\n".join(html_parts) or None
        body = "\n".join(body_parts)
        if not body and html_body:
            body = html_body

        return Email(
            subject=str(message.get("Subject", "")),
            body=body,
            sender=str(message.get("From", "")),
            recipient=str(message.get("To", "")),
            html_body=html_body,
            attachments=attachments,
        )