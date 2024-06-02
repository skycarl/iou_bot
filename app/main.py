"""Main module for IOU Bot."""
import logging
import os

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from . import models
from . import parse_exceptions

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
X_TOKEN = os.environ['X_TOKEN']
HEADERS = {'X-Token': X_TOKEN}
base_url = os.environ.get('APP_URL')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Set logging level to debug
logger.setLevel(logging.DEBUG)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text='Hello to yourself!'
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=('Enter IOUs in the format of: /iou <receiver> <amount> <description>\n\n'
            'e.g., /iou Louie 20.05 if you owe Louie $20.05 for some catnip'))


async def iou(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parse the IOU message and send it to the backend. Parrot back the IOU to the conversation.

    Parameters
    ----------
    update : Update
        The Telegram update object.
    context : ContextTypes.DEFAULT_TYPE
        The Telegram context object.
    """

    logger.debug('Parsing message %s', update.message.text)

    parsed_iou = update.message.text.split(' ')
    receiver = parsed_iou[1]
    amount = parsed_iou[2]
    description = ' '.join(parsed_iou[3:])

    try:
        parsed_iou = models.IOUMessage(
            conversation_id=update.effective_chat.id,
            sender=update.message.from_user.username,
            recipient=receiver,
            amount=amount,
            description=description,
        )
    except parse_exceptions.AmountException as e:
        logger.error(
            'Invalid amount: %s, originating message: %s, parsed amount: %s',
            e,
            update.message.text,
            amount,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='Invalid amount: ' + str(e)
        )
        return
    except Exception as e:
        logger.error(
            'Invalid message: %s, originating message: %s', e, update.message.text
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='Invalid input; try again'
        )
        return

    post_url = base_url + '/entries'
    response = requests.post(post_url, headers=HEADERS, json=parsed_iou.model_dump())

    # Check that the response is 201
    if response.status_code == 201:
        logger.debug('Successfully posted %s', parsed_iou.model_dump())
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"@{update.message.from_user.username} sent {receiver} ${amount} for {description}",
        )
    else:  # TODO clean this up before deployment
        msg = f"Backend error: {response.text}\nmessage: {update.message.text}\nIOUMessage: {parsed_iou.model_dump()}"
        logger.error(msg)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


async def get_iou_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the IOU status between two users from the backend and send the results to the querying conversation.

    Parameters
    ----------
    update : Update
        The Telegram update object.
    context : ContextTypes.DEFAULT_TYPE
        The Telegram context object.
    """

    logger.debug('Parsing query %s', update.message.text)
    parsed_iou = update.message.text.split(' ')
    user1 = parsed_iou[1]
    user2 = parsed_iou[2]

    try:
        parsed_query = models.IOUQuery(
            conversation_id=update.effective_chat.id, user1=user1, user2=user2
        )
    # TODO update this to handle member error bubbled up from backend
    except parse_exceptions.ChatMemberException as e:
        logger.error(
            'Invalid chat member: %s, originating message: %s, parsed users: %s',
            e,
            update.message.text,
            user1 + ' ' + user2,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='Invalid chat member: ' + str(e)
        )
        return
    except Exception as e:
        logger.error(
            'Invalid message: %s, originating message: %s', e, update.message.text
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='Invalid input; try again'
        )
        return

    # TODO clean this up by passing as params: https://stackoverflow.com/a/49520497/12950881
    url = (
        base_url
        + '/iou_status/?conversation_id='
        + str(parsed_query.conversation_id)
        + '&user1='
        + str(parsed_query.user1)
        + '&user2='
        + str(parsed_query.user2)
    )
    try:
        response = requests.get(
            url,
            headers=HEADERS,
        )
    except requests.exceptions.RequestException as e:
        logger.error(
            'Error contacting backend: %s, message: %s, IOUQuery: %s',
            e,
            update.message.text,
            parsed_query.model_dump(),
        )
        # TODO update this message once testing is done
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='An error occurred contacting the backend: ' + str(e),
        )
        return

    # Response validation
    if response.status_code == 200:
        parsed_response = models.IOUResponse(
            conversation_id=update.effective_chat.id,
            user1=response.json()['user1'],
            user2=response.json()['user2'],
            amount=response.json()['amount'],
        )

        await context.bot.send_message(
            chat_id=parsed_response.conversation_id,
            text=f"@{parsed_response.user1} owes @{parsed_response.user2} ${parsed_response.amount}",
        )
    else:
        err_msg = (
            f"Invalid response from backend: {response.text}\n"
            f"message: {update.message.text}\n"
            f"IOUQuery: {parsed_query.model_dump()}"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=err_msg
        )  # TODO update this message once testing is done
        logger.error(err_msg)
        return

    return


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    hello_handler = CommandHandler('hello', hello)
    application.add_handler(hello_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    iou_handler = CommandHandler('iou', iou)
    application.add_handler(iou_handler)

    query_handler = CommandHandler('query', get_iou_status)
    application.add_handler(query_handler)

    application.run_polling()
