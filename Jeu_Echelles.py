"""
-*- coding: utf-8 -*-
Usage : Jeux des echelles et des serpents
Python : 3.10.1
Created on 21/02/2022 by Céleste
"""
import random


# from time import sleep


def player_status():
    """
    Choici le nombre de joueurs humain et de joueurs IA
    :return: list[int, int]
    """
    status: list[int, int] = [0, 0]

    while sum(status) != 4:
        status[0] = int(input('Nombre de joueurs humains svp : '))
        status[1] = int(input('Nombre de joueurs IA svp : '))

    return tuple(status)


def travel(position: int, dices: int, win: int, snakes: list[tuple[int, int]], falls: list[tuple[int, int]]) -> int:
    """
    Déplace le joueur selon qu'il tombe sur un serpent ou une échelle et selon qu'il déplace ou non la valeur gagnable
    :param position: int
    :param dices: int
    :param win: int
    :param snakes: list[tuple[int, int]]
    :param falls: list[tuple[int, int]]
    """
    if position + dices > win:
        position = win - (position + dices - win)
    else:
        position += dices

    for j in range(len(falls)):
        if position == falls[j][0]:
            position = falls[j][1]
            print(f"Vous etes tombé sur une échelle")
            return position

    for j in range(len(snakes)):
        if position == snakes[j][0]:
            position = snakes[j][1]
            print(f"Vous avez pris un serpent")
            return position

    return position


def main(status, snakes: list[tuple[int, int]], falls: list[tuple[int, int]], win: int) -> int:
    """
    Fonction principale du jeu
    :param status: tuple[int, int]
    :param snakes: list[tuple[int, int]]
    :param falls: list[tuple[int, int]]
    :param win: int
    :return: int
    """
    case = [0] * (status[0] + status[1])
    print("-------------------------------------------------------")

    while True:
        for i in range(status[0] + status[1]):
            temp: int = case[i]
            # if i <= status[0]:
            #     input(f'Appuyez sur entrée pour commencer le tour du joueur humain {i + 1}')
            dices: int = random.randint(1, 6)
            print(i)
            print(f'Vous avez fait {dices}')
            print(f'Vous êtes à la case {temp}')
            temp = travel(temp, dices, win, snakes, falls)
            print(f'Vous êtes maintenant à la case {temp}')

            print("-------------------------------------------------------")
            if temp == win:
                print("Vous avez gagné !")
                return i
            case[i] = temp
            # sleep(1)


def game_stats(nb_games: int, nb_players: int, snakes: list[tuple[int, int]], falls: list[tuple[int, int]], win: int) -> None:
    """
    Lancer nb_games du jeu et calcule le % de win d'un joueur, le nombre moyen d'échelles et de serpent pris dans la
    partie et le nombre de tours moyen
    :param nb_games: int
    :param nb_players: int
    :param snakes: list[tuple[int, int]]
    :param falls: list[tuple[int, int]]
    :param win: int
    :return: None
    """
    turn = 0
    snake_proba = 0
    falls_proba = 0
    prob_win = [0] * nb_players

    for game in range(nb_games):
        locations = [0] * nb_players
        while win not in locations:
            for i in range(nb_players):
                turn += 1
                dices = random.randint(1, 6)
                if dices + locations[i] > win:
                    locations[i] = win - (locations[i] + dices - win)
                else:
                    locations[i] += dices

                for j in range(len(falls)):
                    if locations[i] == falls[j][0]:
                        locations[i] = falls[j][1]
                        falls_proba += 1

                for j in range(len(snakes)):
                    if locations[i] == snakes[j][0]:
                        locations[i] = snakes[j][1]
                        snake_proba += 1
                if locations[i] == win:
                    prob_win[i] += 1

        prob_win[locations.index(win)] += 1

    print(f'Le nombre de tours moyen est de {turn / nb_games}')
    print(f'Le nombre de fois où un joueur a pris un serpent est de {snake_proba / nb_games}')
    print(f'Le nombre de fois où un joueur a pris une échelle est de {falls_proba / nb_games}')

    for i in range(nb_players):
        print(f'Le joueur {i + 1} a gagné {round(prob_win[i] / nb_games * 100, 2)}% des parties')


if __name__ == "__main__":
    win = 100
    falls = [(1, 38), (4, 14), (9, 31), (21, 42), (28, 84), (51, 67), (71, 91), (80, 99)]
    snakes = [(17, 7), (54, 19), (62, 24), (64, 34), (87, 60), (93, 73), (95, 75), (98, 79)]
    print("Start")

    if bool(input("Voulez-vous jouer ou calculer les stats du jeu ? (O/N)") == 'N'):
        players = player_status()
        winner = main(players, snakes, falls, win)
        print(f'Le joueur {winner + 1} a gagné')
        print('End')
        input('Applause sur entrée pour quitter')

    else:
        game_stats(10000, 4, snakes, falls, win)
