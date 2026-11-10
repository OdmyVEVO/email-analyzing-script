class Email:
    def __init__(self, subject: str, body: str, sender: str, recipient: str, html_body: str = None):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient = recipient
        self.html_body = html_body

    def __repr__(self):
        return f"Email(subject={self.subject}, body={self.body}, sender={self.sender}, recipient={self.recipient}, html_body={self.html_body})"