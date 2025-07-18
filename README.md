# 🪙 Multi-Coin Discord Tipbot

A **production-ready Discord bot** for tipping, swapping, and managing multiple altcoins.

Supports:  
- 🐶 DOGE (Dogecoin)  
- 🐾 DINGO (Dingocoin)  
- 🌏 terraAUS  
- 🇦🇺 AUS

Built with ❤️ for Dogecoin forks.

---

## ✨ Features
- 💸 **Tip users** in any supported coin  
- 🔄 **Swap coins** at fixed rates  
- 📥 Deposit addresses (auto-generated)  
- 📤 Withdraw to external wallets  
- 🛠 Admin-only commands to manage rates  
- 🐳 Full Docker deployment (easy to run anywhere)

---

## 🚀 Quick Start

### 📦 1. Clone the repo
```bash
git clone https://github.com/yourname/multi-coin-tipbot.git
cd multi-coin-tipbot

⚙️ 2. Configure

Edit bot/config.json:

{
  "coins": {
    "DOGE": {"rpc_url": "http://user:pass@doge-node:22555"},
    "DINGO": {"rpc_url": "http://user:pass@dingo-node:22556"},
    "terraAUS": {"rpc_url": "http://user:pass@terraa-node:22557"},
    "AUS": {"rpc_url": "http://user:pass@aus-node:22558"}
  },
  "exchange_rates": {
    "DOGE->DINGO": 2.5,
    "DINGO->terraAUS": 1.8,
    "terraAUS->AUS": 0.75
  },
  "admins": [123456789012345678],
  "mysql": {
    "host": "db",
    "user": "tipbot",
    "password": "tipbotpass",
    "database": "tipbot"
  },
  "discord_token": "YOUR_DISCORD_BOT_TOKEN"
}

🐳 3. Build & Run

docker-compose up -d --build

The bot will start and connect to Discord.
🛑 4. Stop the Bot

docker-compose down

💬 Commands
Command	Description
/tip	Tip a user some coins
/balance	Show your balances
/deposit	Get your deposit address
/withdraw	Withdraw coins to an external address
/swap	Swap coins at fixed rates
/rates	View current exchange rates
/setrate	(Admin) Set or update exchange rates
🔐 Admin Notes

    Add your Discord ID to admins in config.json for access to /setrate.

    Edit exchange rates on-the-fly with /setrate.

📌 Requirements

    Docker & Docker Compose installed

    Discord bot token (How to create one)

    Dogecoin fork nodes with RPC enabled

🏗 Project Structure

multi-coin-tipbot/
├── bot/
│   ├── commands/         # Slash commands
│   ├── config.json       # Bot configuration
│   ├── db.py             # MySQL wrapper
│   ├── main.py           # Bot entry point
│   ├── rpc_wallet.py     # RPC wallet handler
│   └── utils.py          # Utilities
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

❤️ Credits

    discord.py

    python-bitcoinlib

    Dogecoin Core
