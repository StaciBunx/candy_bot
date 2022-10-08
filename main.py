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

CANDY_QYT, FIRST_TURN, GAME = range(3)


async def start(update, context):
    await update.message.reply_text(
        f'Привет, {update.effective_user.first_name}! Добро пожаловать в игру Candy Crush! '
        'Правила: на столе лежат конфеты. Каждый ход соперники забирают себе некоторое количество. Тот, кто забирает со стола последнюю конфету - проигрывает партию. Нажмите /bye, если передумали играть.')
    await update.message.reply_text(
        'Введите количество конфет в куче:')
    return CANDY_QYT


async def candy_qyt(update, context):
    candy_qyt = update.message.text
    if candy_qyt.isdigit():
        context.user_data['candy_qyt'] = candy_qyt
        await update.message.reply_text(f'Хорошо, в кучке теперь {candy_qyt} конфет.')
        await update.message.reply_text(
            f'Введите максимальное количество конфет в раунд, которое можно вытянуть, но не больше {candy_qyt}:')
        return FIRST_TURN
    else:
        await update.message.reply_text("Вы ввели не число! Попробуйте еще раз:")
        return CANDY_QYT


async def first_turn(update, context):
    max_pull = update.message.text
    candy_qyt = int(context.user_data.get('candy_qyt'))
    if max_pull.isdigit():
        max_pull = int(max_pull)
        if max_pull > candy_qyt:
            await update.message.reply_text(f"Число не может быть больше {candy_qyt}. Попробуйте еще: ")
            return FIRST_TURN
        else:
            context.user_data['max_pull'] = max_pull
            await update.message.reply_text(f'Ок, вытягиваем не больше {max_pull} конфет.')
            await update.message.reply_text('Сейчас выясним, кто ходит первый.')
            await update.message.reply_text('Раз...')
            await update.message.reply_text('Два...')
            await update.message.reply_text('Три...')
            turn = random.randint(1, 2)  # 1 - ход человека, 2 - ход бота
            if turn == 1:
                await update.message.reply_text('Вы начинаете ход!\n'
                                                'Введите, сколько вытянуть конфет:')
                return GAME
            elif turn == 2:
                num = random.randint(1, max_pull)
                candy_qyt -= num
                await update.message.reply_text(f"Ход начинает бот.")
                await update.message.reply_text(f'Бот вытянул {num} конфет. В кучке остается {candy_qyt} конфет.')
                await update.message.reply_text('Введите, сколько вытянуть конфет:')
                context.user_data['candy_qyt'] = candy_qyt
                return GAME
    else:
        await update.message.reply_text("Вы ввели не число! Попробуйте еще раз:")
        return FIRST_TURN


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
            if num > candy_qyt:
                num = random.randint(1, candy_qyt)
            candy_qyt -= num
            context.user_data['candy_qyt'] = candy_qyt
            if candy_qyt > 0:
                await update.message.reply_text(f'Бот вытянул {num} конфет. В кучке остается {candy_qyt} конфет.')
                await update.message.reply_text('Введите, сколько вытянуть конфет:')
                return GAME
            else:
                await update.message.reply_text(f'Бот вытянул {num} конфет и конфет не осталось. Вы выиграли! Игра окончена. Нажмите /start, чтобы сыграть еще раз.')
                return ConversationHandler.END
        if candy_qyt <= 0:
            await update.message.reply_text('В кучке не осталось конфет! Вы проиграли! Игра окончена. Нажмите /start, чтобы сыграть еще раз.')
            return ConversationHandler.END


async def bye(update, context):
    await update.message.reply_text(
        'Хорошо, пока!'
    )
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()

game_conversation_handler = ConversationHandler(
    # точка входа в разговор
    entry_points=[CommandHandler('start', start)],
    states={
        CANDY_QYT: [MessageHandler(~filters.COMMAND, candy_qyt)],
        FIRST_TURN: [MessageHandler(filters.ALL, first_turn)],
        GAME: [MessageHandler(filters.ALL, game)],

    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('bye', bye)],
)

app.add_handler(game_conversation_handler)

print('server start')
app.run_polling()
