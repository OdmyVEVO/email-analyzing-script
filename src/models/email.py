from typing import List, Optional


class EmailAttachment:
    def __init__(self, filename: str, content_type: str, payload: bytes):
        self.filename = filename
        self.content_type = content_type
        self.payload = payload

    def __repr__(self):
        return f"EmailAttachment(filename={self.filename}, content_type={self.content_type}, size={len(self.payload)})"


class Email:
    def __init__(
        self,
        subject: str,
        body: str,
        sender: str,
        recipient: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[EmailAttachment]] = None,
    ):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient = recipient
        self.html_body = html_body
        self.attachments = attachments or []

    def __repr__(self):
        return (
            f"Email(subject={self.subject}, body={self.body}, sender={self.sender}, "
            f"recipient={self.recipient}, html_body={self.html_body}, "
            f"attachments={self.attachments})"
        )