# email-analyzing-script

## Usage

Process one email:

```powershell
python main.py --file path\to\message.eml
```

Process all `.eml` files in a directory:

```powershell
python main.py --directory path\to\emails
```

The script prints the sender, recipient, subject, body, and attachment names. HTML content and attachments are saved under `output/<email-name>/`. Set a different destination with `--output-directory path\to\output`.