# 2- Создайте программу для игры с конфетами человек против человека.

# Условие задачи: На столе лежит 2021 конфета(или сколько вы зададите). Играют два игрока делая ход друг после друга.
#  Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет(или сколько вы зададите). Тот, кто берет последнюю конфету - проиграл.
# Предусмотрите последний ход, ибо там конфет остается меньше.
# a) Добавьте игру против бота
# b) Подумайте как наделить бота ""интеллектом""


import random


def game_begin():
    print('-----------------')
    print("ИГРА НАЧИНАЕТСЯ")
    print('-----------------')


def get_candy_number():
    '''
    Функция проверяет число, которок пользователь вводит для суммы конфет в кучке. Возвращает модуль числа.
    '''
    while True:
        try:
            num = abs(int(input("Введите количество конфет в куче: ")))
            return num
        except ValueError:
            print("Вы ввели не число! Попробуйте еще раз.")


def get_pull_number_max():
    '''
    Функция проверяет число, которок пользователь вводит для макисмального значения. Возвращает модуль числа.
    '''
    while True:
        try:
            num = abs(
                int(input("Введите максимальное количество конфет в раунд, которое можно вытянуть: ")))
            return num
        except ValueError:
            print("Вы ввели не число! Попробуйте еще раз.")


def get_first_turn():
    '''
    Функция рандомно задает, кто будет первым ходить. Возвращает номер игрока.
    '''
    turn = 0
    turn = random.randint(1, 2)
    print(f"Ход начинает {turn} игрок.")
    return turn


def get_first_turn_wbot():
    '''
    Функция рандомно задает, кто будет первым ходить, в игре с компьюетром. Возвращает номер игрока.
    '''
    turn = 0
    turn = random.randint(1, 2)
    if turn == 1:
        print(f"Вы начинаете ход.")
    else:
        print(f"Ход начинает компьютер.")
    return turn


def turn_change(player_num):
    '''
    Функция переключает ходы между игроками, возвращает номер игрока.
    '''
    if player_num == 2:
        player_num = 1
    elif player_num == 1:
        player_num = 2
    return player_num


def start_game():
    print('-----------------')
    print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ CANDY CRUSH")
    print('-----------------')
    answer = input("Вы будете играть с человеком? (да/нет): ")
    if ((answer.lower()) == 'да'):
        print("Ок, усаживайтесь по-удобнее.")
        game_pvp()
    else:
        print("Тогда ваш оппонент - компьютер.")
        game_bot()


def turn_wbot(cnd_pull_max,candy_qt, player):
    while candy_qt > 0:
        if player == 1:
            num = int(input("Сколько вытянуть конфет: "))
            if num > cnd_pull_max:
                print(f"Нельзя брать больше {cnd_pull_max} ")
            if num > candy_qt:
                print(f"Нельзя взять конфет больше чем сейчас в кучке ")
            else:
                candy_qt -= num
                if candy_qt >0:
                    print(f'В кучке {candy_qt} конфет')
                elif candy_qt <= 0:
                    print('В кучке не осталось конфет!')
                    continue
                player = turn_change(player)
                print(f'Переход хода.')
        if player == 2:
            num = random.randint(1, cnd_pull_max)
            if num > candy_qt:
                num = random.randint(1, candy_qt)
            else:
                print('-----------------')
                print(f"Компьютер вытягивает {num} конфет.")
                candy_qt -= num
                if candy_qt > 0:
                    print(f'В кучке {candy_qt} конфет')
                # print('-----------------')
                elif candy_qt <= 0:
                    print('В кучке не осталось конфет!')
                    continue
                player = turn_change(player)
                print(f'Переход хода.')
    return player


def turn(cnd_pull_max, candy_qt, player):
    while candy_qt > 0:
        num = int(input("Сколько вытянуть конфет: "))
        if num > cnd_pull_max:
            print(f"Нельзя брать больше {cnd_pull_max} ")
        if num > candy_qt:
            print(f"Нельзя взять конфет больше чем сейчас в кучке ")
        else:
            print('-----------------')
            candy_qt -= num
            if candy_qt > 0:
                print(f'В кучке {candy_qt} конфет')
            elif candy_qt <= 0:
                print('В кучке не осталось конфет!')
                continue
            player = turn_change(player)
            print(f'Теперь ходит {player} игрок')
            current_player = player
    return candy_qt


def game_pvp():
    '''
    Функция содержит в себе
    '''
    candy_qyt = get_candy_number()
    if candy_qyt == 0:
        print("В кучке нет конфет. Введите число больше нуля.")
        game_pvp()
    else:
        candy_pull_max = get_pull_number_max()
        if candy_pull_max > candy_qyt:
            print(
                "Нельзя вытягивать больше конфет, чем их количество в кучке. Попробуем еще раз.")
            game_pvp()
        elif candy_pull_max == 0:
            print(
                "Если ничего не вытягивать из кучки, то и поиграть не удастся. Введите число больше нуля.")
            game_pvp()
        else:
            game_begin()
            current_player = get_first_turn()
            turn(candy_pull_max, candy_qyt, current_player)
            print(f"Выиграл {turn_change(current_player)} игрок!")
            print('-----------------')
            print("КОНЕЦ ИГРЫ")
            print('-----------------')
            play_more_question = input("Хотите поиграть еще? (да/нет): ")
            if ((play_more_question.lower()) == 'да'):
                start_game()
            else:
                print("Хорошо, пока!")


def game_bot():
    candy_qyt = get_candy_number()
    if candy_qyt == 0:
        print("В кучке нет конфет. Введите число больше нуля.")
        game_bot()
    else:
        candy_pull_max = get_pull_number_max()
        if candy_pull_max > candy_qyt:
            print(
                "Нельзя вытянуть больше конфет, чем их количество в кучке. Введите число меньше!")
            game_bot()
        elif candy_pull_max == 0:
            print(
                "Если ничего не вытягивать из кучки, то и поиграть не удастся. Введите число больше нуля.")
            game_bot()
        else:
            game_begin()
            current_player = get_first_turn_wbot()
            turn_wbot(candy_pull_max,candy_qyt,current_player)
            if current_player == 1:
                print("Вы проиграли")
            else:
                print("Вы выиграли!")
            print('-----------------')
            print("КОНЕЦ ИГРЫ")
            print('-----------------')
            play_more_question = input("Хотите поиграть еще? (да/нет): ")
            if ((play_more_question.lower()) == 'да'):
                start_game()
            else:
                print("Хорошо, пока!")


start_game()
