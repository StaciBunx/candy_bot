import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, MessageHandler, filters, ConversationHandler
from config import TOKEN
from game import *

logging.basicConfig(filename='log.txt',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )


CANDY_QYT, MAX_PULL, FIRST_TURN, PLAYER_TURN, BOT_TURN = range(5)


async def rules(update, context):
    await context.bot.send_message(update.effective_chat.id, 'Правила игры: на столе лежат конфеты. Каждый ход соперники забирают со стола конфеты. Тот, кто забирает со стола последнюю конфету - проигрывает партию')


async def start(update, context):
    await update.message.reply_text(
        f'Привет, {update.effective_user.first_name}!\n'
        'Добро пожаловать в игру Candy Crush!\n'
        'Чтобы узнать правила игры нажмите /rules.\n'
        'Нажмите /bye, чтобы закончить разговор.')
    await update.message.reply_text(
        'Введите количествово конфет в куче: ')
    return CANDY_QYT


async def candy_qyt(update, context):
    user = update.message.from_user
    candy_qyt = update.message.text
    await update.message.reply_text(f'Хорошо, в кучке теперь {candy_qyt} конфет')
    await update.message.reply_text(
        f'Введите максимальное количество конфет в раунд, которое можно вытянуть, не больше {candy_qyt}:')
    return MAX_PULL


async def max_pull(update, context):
    user = update.message.from_user
    max_pull = update.message.text
    await update.message.reply_text(f'Ок, вытягиваем не больше {max_pull} конфет')
    return FIRST_TURN

async def first_turn():
    return PLAYER_TURN

async def player_turn():
    return BOT_TURN

async def bot_turn():
    return PLAYER_TURN


async def bye(update, context):
    user = update.message.from_user
    await update.message.reply_text(
        'Хорошо, пока!'
        ,
    )
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()


game_conversation_handler = ConversationHandler(
    # точка входа в разговор
    entry_points=[CommandHandler('start', start)],
    # этапы разговора, каждый со своим списком обработчиков сообщений
    states={
        CANDY_QYT: [MessageHandler(filters.Regex(r'\d+'), candy_qyt)],
        MAX_PULL: [MessageHandler(filters.Regex(r'\d+'), max_pull)],
        FIRST_TURN:[],
        PLAYER_TURN:[],
        BOT_TURN:[]
    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('bye', bye)],)

app.add_handler(game_conversation_handler)

print('server start')
app.run_polling()
