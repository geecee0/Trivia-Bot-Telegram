# Trivia Bot Telegram

A personalized version of the trivia bot, offering random quizzes in private chat or groups with an upgraded ranking system. This fork diverges from the original by integrating The Trivia API (https://the-trivia-api.com/) instead of Open Trivia DB, and keeps track of questions previously asked to prevent repeated questions.

[![GitHub issues](https://img.shields.io/github/issues/geecee0/Trivia-Bot-Telegram)](https://github.com/geecee0/Trivia-Bot-Telegram/issues)
[![GitHub forks](https://img.shields.io/github/forks/geecee0/Trivia-Bot-Telegram)](https://github.com/geecee0/Trivia-Bot-Telegram/network)
[![GitHub stars](https://img.shields.io/github/stars/geecee0/Trivia-Bot-Telegram)](https://github.com/geecee0/Trivia-Bot-Telegram/stargazers)
[![GitHub license](https://img.shields.io/github/license/geecee0/Trivia-Bot-Telegram)](https://github.com/geecee0/Trivia-Bot-Telegram/blob/main/LICENSE)

## What is it?

The Trivia Bot sends quizzes to chat groups or personal chats. If someone answers correctly, they earn points. The bot can also send a ranking with all members in the group and their accumulated points. 

## How to clone bot and setup

1. Download bot files from: <https://github.com/geecee0/Trivia-Bot-Telegram/archive/refs/heads/main.zip>

2. Extract it and open the folder.

3. Create a file named **credentials.py** with the DB credentials and Telegram Token:

    ```python
    telegram_token = "" # Telegram Bot Token
    db_host = ""        # Database host name
    db_name = ""        # Database database name
    db_user = ""        # Database user name
    db_password = ""    # Database user password
    ```

4. Create a MySQL DB or similar like MariaDB, and execute the following query in the database:

    ```SQL
    CREATE TABLE `ranking` (
    `user_id` bigint NOT NULL,
    `chat_id` bigint NOT NULL,
    `username` varchar(50) NOT NULL,
    `date` datetime NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Start the bot:

    ```bash
    python bot.py
    ```

------------

# FAQ

## How to install Python?

Visit [Python's official website](https://www.python.org/downloads/) and install the version for your PC.

## How to install a MySQL DB?

You might choose to install [XAMPP](https://www.apachefriends.org/download.html), as an example. 

## How to create a Telegram Bot?

Refer to the [Telegram Official Guide](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

## Are there any commands?

Yes, there are commands:

```
start - Start the bot
quiz - Send a quiz
help - Send help message
ranking - Send the ranking of the chat
points - Send the sum of your points
vote - Vote the bot in BotsArchive
code - Project's GitHub Page
```

## Problems?

Please report any issues you encounter here: <https://github.com/geecee0/Trivia-Bot-Telegram/issues>
