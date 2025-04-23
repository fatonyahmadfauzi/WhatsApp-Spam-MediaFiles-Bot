# WhatsApp Multi-File Sender Bot

📦 Automated tool to send multiple files via WhatsApp Web with customizable intervals and status tracking

![WhatsApp File Sender Demo](demo.gif) _Example usage animation_

## Features

- **Multi-file support** - Send multiple files in one batch
- **Flexible input** - Add files until you type "selesai"
- **Progress tracking** - Real-time status for each file
- **Customizable** - Set repeat counts and delays
- **Bot status** - Optional timestamps and counters

## Prerequisites

- Python 3.8+
- Google Chrome
- WhatsApp Web account
- Stable internet connection

## Installation

1. Clone repository:

```bash
git clone -b multi-file --single-branch https://github.com/fatonyahmadfauzi/WhatsApp-Spam-MediaFiles-Bot.git WhatsApp-Spam-MediaFiles-Bot_Multi-MediaFiles

cd wWhatsApp-Spam-MediaFiles-Bot_Multi-MediaFiles
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python whatsapp_mediafiles.py
```

Follow the interactive prompts:

1. Scan QR code when prompted
2. Enter recipient/group name (exact match)
3. Add files (one by one, type "selesai" when done)
4. Configure sending parameters

## Configuration Options

| **Parameter**  | **Description**                   | **Example Value**      |
| -------------- | --------------------------------- | ---------------------- |
| Recipient Name | Exact WhatsApp contact/group name | "Family Group"         |
| File Paths     | Multiple file paths               | "doc.pdf", "image.jpg" |
| Repeat Count   | Times to repeat sending           | 3                      |
| Send Interval  | Delay between sends (seconds)     | 5.0                    |
| Upload Delay   | File upload wait time (seconds)   | 3.0                    |
| Bot Status     | Add status messages (Y/N)         | Y                      |

## Ethical Use

**⚠️ Important:**

- This tool is for **legitimate personal/educational use only**
- Do **not** use for spamming or harassment
- Respect WhatsApp's [Terms of Service]()
- Includes automatic delays to prevent rate limiting

## Issue Solution

| **Issue**            | **Solution**                                          |
| -------------------- | ----------------------------------------------------- |
| QR code not scanning | Ensure no other WhatsApp Web session is active        |
| File not found       | Use absolute paths or drag & drop files into terminal |
| Element not found    | Update Chrome and chromedriver to latest versions     |

## License

[MIT License]()
