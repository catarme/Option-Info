#!/usr/bin/python3
# -*- coding: utf-8 -*-

def structure_donne(nb_players: int) -> list[list[str, int, tuple[int, int], list[int], list[int]]]:
    """
    Crée les paramètres de départ de chaque joueur.

    :param nb_players: Nombre de joueurs.
    :type nb_players: int
    :return: liste de liste de la couleur, nombre de pion que le joueur a en main, (case d'entrée vers le homerun, case de sortie de la maison), position des pion sur le plateau, position des pions dans le home run
    :Example:
    >>> structure_donne(2)
    [['bleu', 4, (1, 3), [], []], ['vert', 4, (27, 29), [], []]]
    """
    couleur: list[str] = ["bleu", "rouge", "vert", "jaune"]
    players: list[list[str, int, tuple[int, int], list[int], list[int]]] = []

    if nb_players == 2:
        couleur = ["bleu", "vert"]
        players.append([couleur[0], 4, (1, 3), [], []])
        players.append([couleur[1], 4, (27, 29), [], []])
        return players

    else:
        for x in range(0, nb_players, 1):
            players.append([couleur[x], 4, (1 + (x * 13), 3 + (x * 13)), [], []])

    print(players)
    return players


def deplacement_piece(player: list[list[str, int, tuple[int, int], list[int], list[int]]], des: int, piece: int, i: int) -> \
list[list[str, int, tuple[int, int], list[int], list[int]]]:
    """
    deplace les pions du joueur en fonction de la valeur de dé.

    :param player: liste de la couleur, nombre de pion que le joueur a en main, (case d'entrée vers le homerun, case de sortie de la maison), position des pion sur le plateau, position des pions dans le home run
    :param des: valeur de dé
    :param piece: numéro du pion à déplacer
    :param i: numéro du joueur
    :return: liste de la couleur, nombre de pion que le joueur a en main, (case d'entrée vers le homerun, case de sortie de la maison), position des pion sur le plateau, position des pions dans le home run
    :Example:
    >>> deplacement_piece([['bleu', 4, (1, 3), [], []], ['vert', 4, (27, 29), [], []]], 3, 0, 0)
    [['bleu', 4, (1, 3), [], []], ['vert', 4, (27, 29), [], []]]
    """

    # Regarde si la position du pion + des ne dépasse pas la case player[i][2][0]
    home_run: bool = False
    place: int = player[i][3][player[i][3].index(piece)]


    for y in range(des):
        #If the counter in question is on the board
        if not home_run:
            player[i][3][player[i][3].index(piece)] += 1
            if player[i][3][player[i][3].index(piece)] > 52:
                player[i][3][player[i][3].index(piece)] %= 52

            if player[i][3][player[i][3].index(piece)] > player[i][2][0]:
                # Transfer the pawn to the homerun
                player[i][4].append(1)
                # Remove the pawn from the list of pawns
                player[i][3].remove(player[i][3][player[i][3].index(piece)])
                home_run = True
        else:
            # If it is in the homerun then it is advanced
            player[i][4][player[i][4].index(piece)] += 1

    if not home_run:
        # Look at every piece of every player except the one who threw the dice
        for x in range(0, len(player), 1):
            if x != i:
                # We check the position of each piece one by one if it is on the same one that the player has just moved.
                for y in range(0, len(player[x][3]), 1):
                    if player[x][3][y] == player[i][3][player[i][3].index(piece)]:
                        # Then we remove this value and increase the coin value in the pocket of the opposite player
                        player[x][3].remove(player[x][3][y])
                        player[x][1] += 1

    print(player)
    return player


if __name__ == "__main__":
    nb_player = int(input("Combien de joueurs ? "))
    while nb_player < 2 or nb_player > 4:
        print("Veuillez entrer un nombre de joueurs compris entre 2 et 4")
        nb_player = int(input("Combien de joueurs ? "))

    player = structure_donne(nb_player)

    # Commence la partie
    while True:
        for i in range(len(player) - 1):
            print(f"C'est au tour de {player[i][0]}")
            # Affiche les données du joueur
            print(f"vos données sont : {player[i]}")

            # Lance le dé
            from random import randint

            des: int = randint(1, 6)
            print(f"Vous avez fait {des}")

            if des == 6:
                if input(f"Vous avez fait un 6, voulez vous sortir une piece ? (o/n) ") == "o":
                    print(f"Vous avez sorti une piece à la case {player[i][2][0]}")
                    # Ajoute la piece sur la case de sortie
                    player[i][3].append(player[i][2][0])

                    player[i][1] -= 1
                    continue
                elif player[i][3] == [] and player[i][4] == []:
                    print(f"Vous n'avez pas de piece sorti, vous passez votre tour")
                    continue

            if player[i][3] != [] or player[i][4] != []:
                print(f"Vous avez fait {des}")
                print(f"Vous avez {player[i][3]} pieces sur le plateau")
                print(f"Vous avez {player[i][4]} pieces sur le homerun")

            if player[i][4]:
                # Demande au joueur si il veut déplacer une piece du homerun
                if input(f"Voulez vous déplacer une piece du homerun ? (o/n) ") == "o":
                    # Demande à l'utilisateur de choisir une piece du homerun
                    piece: int = int(input("Quelle piece voulez vous déplacer ? "))
                    while piece not in player[i][4]:
                        print("Vous n'avez pas cette piece dans le homerun")
                        piece = int(input("Quelle piece voulez vous déplacer ? "))

                    player = deplacement_piece(player, i, piece, des)
                    continue

            if player[i][3]:
                # Demande au joueur si il veut déplacer une piece du plateau
                if input(f"Voulez vous déplacer une piece du plateau ? (o/n) ") == "o":
                    # Demande à l'utilisateur de choisir une piece du plateau
                    piece: int = int(input("Quelle piece voulez vous déplacer ? "))
                    while piece not in player[i][3]:
                        print("Vous n'avez pas cette piece sur le plateau")
                        piece = int(input("Quelle piece voulez vous déplacer ? "))

                    player = deplacement_piece(player, piece, des, i)
                    continue

            # Regarde si il ya 4 pions sur la case 6 dans le home run du joueur
            if player[i][4] == [6, 6, 6, 6]:
                print(f"Vous avez gagné, vous avez {player[i][1]} pieces sur le plateau")
                break
