#!/usr/bin/env python

from datetime import datetime
import logging
import requests

from credentials import telegram_token, db_host, db_name, db_user, db_password
from telegram import ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    MessageHandler,
    Filters,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context):
    """Inform user about what this bot can do"""
    if update.effective_chat.type == "private":
        update.message.reply_text(
            "Hi " + update.effective_user.name +
            " 👋! I'm a trivia bot. I can give you a quiz. Use /quiz to get a quiz."
        )
    else:
        update.message.reply_text(
            "Hi " + update.effective_chat.title +
            " 👋! I'm a trivia bot. I can give you a quiz and send a group ranking. Use /quiz to get a quiz."
        )

def quiz(update, context):
    """Send a quiz"""
    response = requests.get("https://the-trivia-api.com/v2/questions")
    if response.status_code == 200:
        questions = response.json().get("results", [])
        if questions:
            selected_question = questions[0]
            all_options = selected_question.get("incorrect_answers", [])
            all_options.append(selected_question.get("correct_answer", ""))
            random.shuffle(all_options)
            correct_position = all_options.index(selected_question["correct_answer"])
            message = update.message.reply_poll(
                f"❔ Category: {selected_question['category']}\n⚠️ Difficulty: {selected_question['difficulty']}\n{selected_question['question']}",
                all_options,
                type="quiz",
                correct_option_id=correct_position,
                is_anonymous=False,
            )
            # Save some info about the poll the bot_data for later use in receive_quiz_answer
            payload = {
                message.poll.id: {
                    "chat_id": update.effective_chat.id,
                    "message_id": message.message_id,
                    "questions": all_options,
                    "correct_option_id": correct_position,
                }
            }
            context.bot_data.update(payload)
    else:
        update.message.reply_text("Failed to fetch trivia questions.")



def receive_quiz_answer(update, context):
    """Receive the answer to a quiz"""
    # Get the poll id from the message
    poll_id = update.poll_answer.poll_id
    # Get the payload from the bot_data
    payload = context.bot_data.get(poll_id)
    if payload:
        # Get the chat_id and message_id from the payload
        chat_id = payload["chat_id"]
        # Get the correct_option_id from the payload
        correct_option_id = payload["correct_option_id"]
        # Get the answer from the user
        answer = update.poll_answer.option_ids[0]
        # Check if the answer is correct
        if answer == correct_option_id:
            # Add a point for correct answer
            add_point(update.poll_answer.user.id, chat_id, update.poll_answer.user.username)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a help message"""
    await update.message.reply_text("Use /quiz to get a quiz.\nUse /ranking to get the ranking.\nUse /help to get this message.\nUse /start to get this message.\nUse /points to get the sum of your points.\nUse /vote for voting bot, /code for get the code Github page.")

async def vote_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a call-to-action vote message"""
    await update.message.reply_text("If you like the bot, please vote me here: https://t.me/BotsArchive/2474 ")

async def github_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display Github Page message"""
    await update.message.reply_text("If you want see or make a pull request, here the Github Page of the Bot: https://github.com/Kekko01/Trivia-Bot-Telegram ")


async def add_point(user_id, chat_id, username) -> None:
    """Add a point to the user"""
    mydb = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO ranking (user_id, chat_id, username, date) VALUES (%s, %s, %s, %s)"
    val = (user_id, chat_id, username, datetime.now())
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "UPDATE ranking SET username = %s WHERE user_id = %s"
    val = (username, user_id)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()

async def get_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text("⚠️ This command is only for groups.")
    else:
        """Display the ranking"""
        mydb = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
        )
        mycursor = mydb.cursor()
        sql = "SELECT username, count(date) AS points FROM ranking WHERE chat_id = " + str(update.effective_chat.id) + " GROUP BY username ORDER BY points DESC"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        ranking = "🏅 This is the top 10 ranking for the chat " + update.effective_chat.title + ":\n"
        position = 1
        actual_points = myresult[0][1]
        for row in myresult:
            if row[1] < actual_points:
                position += 1
                actual_points = row[1]
            if position <= 10:
                ranking += str(position) + ") [" + row[0] + "](https://t.me/" + row[0] + "): " + str(row[1]) + " points\n"
        await update.message.reply_text(ranking, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        mycursor.close()
        mydb.close()

async def get_my_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the ranking"""
    mydb = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    mycursor = mydb.cursor()
    sql = "SELECT count(date) AS points FROM ranking WHERE user_id = " + str(update.effective_user.id) + " GROUP BY username"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    try:
        ranking = "You have " + str(myresult[0][0]) + " points! 🧮\n"
    except IndexError:
        ranking = "You have no points! ❎\n"
    await update.message.reply_text(ranking)
    mycursor.close()
    mydb.close()


def main():
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(CommandHandler("help", help_handler))
    dp.add_handler(PollAnswerHandler(receive_quiz_answer))
    dp.add_handler(CommandHandler("ranking", get_ranking))
    dp.add_handler(CommandHandler("points", get_my_points))
    dp.add_handler(CommandHandler("vote", vote_bot))
    dp.add_handler(CommandHandler("code", github_page))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
