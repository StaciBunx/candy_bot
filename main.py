import logging
import random
from telegram import *
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from config import TOKEN


logging.basicConfig(filename='log.txt',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

CANDY_QYT, MAX_PULL, FIRST_TURN, GAME = range(4)


async def start(update, context):
    await update.message.reply_text(
        f'Привет, {update.effective_user.first_name}!\n'
        'Добро пожаловать в игру Candy Crush!\n'
        'Правила: на столе лежат конфеты. Каждый ход соперники забирают со стола конфеты. Тот, кто забирает со стола последнюю конфету - проигрывает партию.'
        'Нажмите /bye, чтобы закончить разговор.')
    await update.message.reply_text(
        'Введите количествово конфет в куче:')
    return CANDY_QYT


async def candy_qyt(update, context):
    candy_qyt = update.message.text
    await update.message.reply_text(f'Хорошо, в кучке теперь {candy_qyt} конфет.')
    await update.message.reply_text(
        f'Введите максимальное количество конфет в раунд, которое можно вытянуть, не больше {candy_qyt}:')
    context.user_data['candy_qyt'] = candy_qyt
    return MAX_PULL


async def max_pull(update, context):
    max_pull = update.message.text
    await update.message.reply_text(f'Ок, вытягиваем не больше {max_pull} конфет.\n'
                                    'Нажмите /next чтобы продолжить.')
    context.user_data['max_pull'] = max_pull
    return FIRST_TURN


async def first_turn(update, context):
    await update.message.reply_text('Сейчас выясним, кто ходит первый.')
    await update.message.reply_text('Раз...')
    await update.message.reply_text('Два...')
    await update.message.reply_text('Три...')
    turn = random.randint(1, 2)
    if turn == 1:
        await update.message.reply_text('Вы начинаете ход!\n'
                                        'Введите, сколько вытянуть конфет:')
        return GAME
    else:
        await update.message.reply_text(f"Ход начинает бот.")
        candy_qyt = int(context.user_data.get('candy_qyt'))
        max_pull = int(context.user_data.get('max_pull'))
        num = random.randint(1, max_pull)
        candy_qyt -= num
        await update.message.reply_text(f'Бот вытягивает {num} конфет. В кучке остается {candy_qyt} конфет.')
        await update.message.reply_text('Введите, сколько вытянуть конфет:')
        context.user_data['candy_qyt'] = candy_qyt
        return GAME


async def game(update, context):
    num = int(update.message.text)
    candy_qyt = int(context.user_data.get('candy_qyt'))
    max_pull = int(context.user_data.get('max_pull'))
    if num > max_pull:
        await update.message.reply_text(f"Нельзя брать больше {max_pull}.")
        await update.message.reply_text('Введите, сколько вытянуть конфет:')
        return GAME
    if num > candy_qyt:
        await update.message.reply_text(f"Нельзя взять конфет больше чем сейчас в кучке.")
        await update.message.reply_text('Введите, сколько вытянуть конфет:')
        return GAME
    else:
        candy_qyt -= num
        context.user_data['candy_qyt'] = candy_qyt
        if candy_qyt > 0:
            await update.message.reply_text(f'Теперь в кучке {candy_qyt} конфет.')
            num = random.randint(1, max_pull)
            candy_qyt -= num
            context.user_data['candy_qyt'] = candy_qyt
            await update.message.reply_text(f'Бот вытягивает {num} конфет. В кучке остается {candy_qyt} конфет.')
            await update.message.reply_text('Введите, сколько вытянуть конфет:')
            return GAME
        elif candy_qyt <= 0:
            await update.message.reply_text('В кучке не осталось конфет! Вы проиграли!')
            return ConversationHandler.END

async def bye(update, context):
    user = update.message.from_user
    await update.message.reply_text(
        'Хорошо, тогда в другой раз!',
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
        FIRST_TURN: [CommandHandler('next', first_turn)],
        GAME: [MessageHandler(filters.Regex(r'\d+'), game)],

    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('bye', bye)],
)

app.add_handler(game_conversation_handler)

print('server start')
app.run_polling()
