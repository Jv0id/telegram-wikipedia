# Telegram Wikipedia Bot
| main                                                                                                                       | 
|----------------------------------------------------------------------------------------------------------------------------|
| ![`main` tests](https://github.com/denis-shvetcov/telegram-wikipedia/actions/workflows/pipeline.yml/badge.svg?branch=main)  |
## Description
A bot for using wikipedia right in the telegram app

## How to use the bot

This bot receives your message and does a quick wikipedia search, giving you a short summary.
Available commands:

- `/start` — exchange greetings with the bot:


- `/help` — see available commands:


- `/en` search articles in English:


- `/chinese` — search articles in Chinese:


## Getting started

### Setting up credentials

First, go to the [BotFather](https://t.me/BotFather) and get your own bot token.
After that, you need to input it to `API_TOKEN` variable in `main.py`.

### Run the app with Docker

To run the bot with Docker, just follow this steps.

Run the application, passing your API token:

```
docker run -d -e API_TOKEN='YOUR_TOKEN' jp0id/telegram-wikipedia
```
For this to work, you have to store your API token as an environment variable.

### Running without Docker

To begin, clone this repository:
```
git clone https://github.com/jv0id/telegram-wikipedia.git
```
Then follow this steps:
- Get Python `ver. 3.10` or newer
- Run the requirements installation `pip install -r requirements.txt`
- Run the main file `python main.py`

Now you're all set. Have fun.

