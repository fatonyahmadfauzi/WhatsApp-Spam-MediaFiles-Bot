# WhatsApp File Sender Bot

A Selenium-based automation tool to send files repeatedly through WhatsApp Web with customizable intervals and status messages.

## Features

- Send files multiple times with configurable delays
- Add bot status messages with timestamps
- Supports both individual chats and groups
- Automatic QR code scanning detection
- Progress tracking and success/failure reporting

## Prerequisites

- Python 3.8+
- Google Chrome browser
- Stable internet connection

## Installation

1. Clone the repository:

```bash
git clone -b single-file --single-branch https://github.com/fatonyahmadfauzi/WhatsApp-Spam-MediaFiles-Bot.git WhatsApp-Spam-MediaFiles-Bot_Single-MediaFiles

cd WhatsApp-Spam-MediaFiles-Bot_Single-MediaFiles
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:

```bash
python whatsapp_mediafiles.py
```

2. Follow the on-screen instructions:
   - Scan the QR code when prompted
   - Enter recipient name (exactly as in WhatsApp)
   - Provide file path
   - Set sending parameters

## Configuration Options

| **Parameter**  | **Description**                 | **Default** |
| -------------- | ------------------------------- | ----------- |
| Recipient Name | Exact name of contact/group     | -           |
| File Path      | Absolute or relative file path  | -           |
| Repeat Count   | Number of times to send         | 1           |
| Interval       | Delay between sends (seconds)   | 1.0         |
| Upload Delay   | File upload wait time (seconds) | 3.0         |
| Bot Prompt     | Add status messages (Y/N)       | N           |

## Troubleshooting

- **QR Code Not Scanning**: Ensure WhatsApp Web isn't already logged in elsewhere
- **Element Not Found**: Check if WhatsApp Web's interface has changed
- **File Not Sending**: Verify file path is correct and accessible

## Disclaimer

This is for educational purposes only. Use responsibly and in compliance with WhatsApp's Terms of Service.

## License

MIT License
