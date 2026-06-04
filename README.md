# 🔍 ReconPulse - Advanced OSINT Platform

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)

---

## 📊 Overview

**ReconPulse** is an enterprise-grade OSINT investigation platform that extracts **100% of available intelligence** from email addresses using the IntelBase API.

---

## 🚀 Quick Start

```bash
git clone https://github.com/0xMedl/Reconpulse.git
cd Reconpulse
pip install -r requirements.txt
echo "INTELBASE_API_KEY=your_api_key" > .env
python -m reconpulse
```

---

## 📖 Usage

```bash
# Interactive mode
python -m reconpulse

# Single investigation
python -m reconpulse user@example.com

# Export formats
python -m reconpulse user@example.com json
python -m reconpulse user@example.com csv
python -m reconpulse user@example.com html

# Batch processing
python -m reconpulse batch emails.txt
```

---

## ✨ Features

**Intelligence Gathering:**
- 📧 Complete email profiling & metadata
- 👤 Account discovery across 500+ services
- 🔓 Full data breach analysis with credentials
- 🦠 Stealer log & malware detection
- 📅 Activity timeline reconstruction

**Analysis & Export:**
- 📈 Risk scoring (0-100) with threat levels
- 🔑 Password strength & reuse analysis
- 📄 Multi-format export (JSON/CSV/HTML)
- 🎨 Professional Rich-powered terminal UI
- 📦 Batch investigation support

---

## 📊 Data Extracted

| Category | Details |
|----------|---------|
| **Meta** | First seen, last seen, activity |
| **Accounts** | Usernames, IDs, profile URLs, creation dates, followers, locations |
| **Breaches** | Passwords, usernames, IPs, names, phones, hashes |
| **Stealer Logs** | Malware infections, compromised data |
| **Validator** | 500+ service registration checks |
| **Timeline** | Chronological events |

---

## 📁 Project Structure

```
Reconpulse/
├── reconpulse/
│   ├── core/
│   │   ├── api_client.py
│   │   └── engine.py
│   ├── display/
│   │   └── terminal_ui.py
│   ├── export/
│   │   └── exporter.py
│   ├── utils/
│   │   ├── constants.py
│   │   └── helpers.py
│   └── cli.py
├── requirements.txt
└── README.md
```

---

## 🔧 Requirements

- Python 3.8+
- `requests`
- `rich`
- IntelBase API key

---

## ⚠️ Disclaimer

**For authorized security research only.** Always obtain proper authorization.

---

## 📄 License

MIT License

---

## 🌟 Credits

- Powered by [IntelBase API](https://intelbase.is)
- Created by [0xMedl](https://github.com/0xMedl)
