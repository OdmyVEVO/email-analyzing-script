import argparse
from pathlib import Path

from src.file.parse import FileParser
from src.file.read import DirectoryReader
from src.file.save import EmailWriter
from src.models.file import File


def process_email_file(file: File, output_directory: str) -> None:
    email = FileParser(file).parse()
    if email is None:
        return
    print(f"From: {email.sender}")
    print(f"To: {email.recipient}")
    print(f"Subject: {email.subject}")
    print("Body:")
    print(email.body)
    print("Attachments:")
    if email.attachments:
        for attachment in email.attachments:
            print(f"- {attachment.filename} ({attachment.content_type})")
    else:
        print("- none")

    result_directory = EmailWriter(output_directory).save(email, file.name)
    if email.html_body is not None:
        print(f"HTML saved to: {result_directory / 'email.html'}")
    if email.attachments:
        print(f"Attachments saved to: {result_directory / 'attachments'}")

def main():
    parser = argparse.ArgumentParser(description="Email Analyzer")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", help="Path to the email file")
    input_group.add_argument("--directory", help="Path to the directory containing email files")
    parser.add_argument("--output-directory", default="output", help="Directory for HTML and attachments")
    args = parser.parse_args()

    if args.file:
        file_path = Path(args.file)
        if not file_path.is_file():
            parser.error(f"not a file: {file_path}")
        file = File(
            name=file_path.name,
            size=file_path.stat().st_size,
            path=str(file_path.resolve()),
        )
        process_email_file(file, args.output_directory)
    else:
        directory_path = Path(args.directory)
        if not directory_path.is_dir():
            parser.error(f"not a directory: {directory_path}")
        for file in DirectoryReader(str(directory_path)).list_files():
            process_email_file(file, args.output_directory)

if __name__ == "__main__":
    main()