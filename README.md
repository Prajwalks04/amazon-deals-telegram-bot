# Amazon Deals Telegram Bot

## Overview
This repository contains a Telegram bot that fetches and shares the latest Amazon deals. The bot is built using Python and Docker.

## Features
- Fetch latest deals from Amazon
- Share deals on Telegram
- Customizable settings for deal notifications

## Installation

### Prerequisites
- Python 3.x
- Docker

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Prajwalks04/amazon-deals-telegram-bot.git
    cd amazon-deals-telegram-bot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables. Create a `.env` file and add your Telegram bot token and Amazon API details:
    ```plaintext
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    AMAZON_API_KEY=your_amazon_api_key
    ```

5. Run the bot:
    ```bash
    python bot.py
    ```

### Using Docker
Alternatively, you can use Docker to run the bot:
1. Build the Docker image:
    ```bash
    docker build -t amazon-deals-telegram-bot .
    ```

2. Run the Docker container:
    ```bash
    docker run -d --env-file .env amazon-deals-telegram-bot
    ```

## Usage
Once the bot is running, you can start interacting with it on Telegram. Use the bot commands to get the latest deals.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
