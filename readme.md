<div align="center">
  <img src="https://ibb.co/QKVKrTv" alt="Hydra Logo" width="150"/>

  # Hydra Discord Bot Adder

  <p>A lightweight, multi-threaded Discord bot deployment tool with automated captcha solving.</p>

  <p>
    <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="Version"/>
    <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge" alt="Python"/>
    <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License"/>
  </p>
</div>

---

## ⚡ Features

- 🚀 Multi-threaded
- 🤖 Auto Captcha
- 📝 Logging
- 🔒 Proxy Support
- 🛠️ Easy setup with `start.bat`

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nuu-maan/Hydra-Discord-Bot-Adder.git
   cd hydra
   ```
2. **Prepare the environment**
   Place the following files in the `data` folder:
   - `config.json` for configuration
   - `guild_ids.txt` for server IDs (one per line)
   - `req.txt` listing Python dependencies

3. **Install dependencies**
   Simply run `start.bat`. It will:
   - Install required dependencies from `req.txt`
   - Start the `hydra.py` script

4. **Get RazorCap API Key**
   [Get your API key here](https://razorcap.xyz/dashboard).

5. **Configure the tool**
   Edit `config.json` in the `data` folder:
   ```json
   {
       "token": "your_discord_token",
       "razorcap_key": "your_razorcap_api_key",
       "proxy": "user:pass@ip:port",
       "permission": "8",
       "clientIds": ["bot_id_1", "bot_id_2"],
       "threads": 1
   }
   ```

---

## 🚀 Usage

Run the tool by double-clicking `start.bat`.

---

## ⚠️ Disclaimer

This tool is for educational purposes only. Users must comply with Discord's Terms of Service.

---

<div align="center">
  <p>Created by <a href="https://github.com/Nuu-maan">Numan</a></p>
  <a href="https://github.com/Nuu-maan/Hydra-Discord-Bot-Adder/issues">Report Bug</a> •
  <a href="https://github.com/Nuu-maan/Hydra-Discord-Bot-Adder/issues">Request Feature</a>
</div>
