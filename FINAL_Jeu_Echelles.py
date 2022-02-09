"""
-*- coding: utf-8 -*-
Usage : Jeux des echelles et des serpents
Python : 3.10.1
Created on 04/02/2022 by Céleste
"""

from random import randint


def player_status() -> tuple[int]:
    """
    Choici le nombre de joueurs humain et de joueurs IA
    :return: list[int, int]
    """
    status: list[int] = [0, 0]

    while sum(status) != 4:
        status[0] = int(input('Nombre de joueurs humains svp : '))
        status[1] = int(input('Nombre de joueurs IA svp : '))

    return tuple(status)


def main(status: tuple[int] = (0, 4)) -> int:
    """
    Fonction principale du jeu
    :param status: list[int] = (0, 4)
    :return: int
    """
    locations: list[int] = [0] * sum(status)
    win: int = 100

    while True:
        for i in range(sum(status)):
            if i <= status[0]:
                input(f'Appuyez sur entrée pour commencer le tour du joueur humain {i + 1}')
            dices = randint(1, 6)
            if dices + locations[i] > 100:
                locations[i] = 100 - (locations[i] + dices - 100)
            else:
                locations[i] += dices
            print(f'Vous avez fait {dices}')
            print(f'Vous êtes à la case {locations[i]}')

            falls = [(1, 38), (4, 14), (9, 31), (21, 42), (28, 84), (51, 67), (71, 91), (80, 99)]
            snakes = [(17, 7), (54, 19), (62, 24), (64, 34), (87, 60), (93, 73), (95, 75), (98, 79)]

            for j in range(len(falls)):
                if locations[i] == falls[j][0]:
                    locations[i] = falls[j][1]
                    print(f'Vous etes tombé sur une échelle et êtes à la case {locations[i]}')
                    break

            for j in range(len(snakes)):
                if locations[i] == snakes[j][0]:
                    locations[i] = snakes[j][1]
                    print('Vous avez pris un serpent et êtes à la case {}'.format(locations[i]))

            if locations[i] == win:
                print("Vous avez gagné !")
                return i


if __name__ == "__main__":
    print("Start")
    players = player_status()

    winner = main(players)

    print(f'Le joueur {winner + 1} a gagné')
    print('End')
    input('Applause sur entrée pour quitter')
