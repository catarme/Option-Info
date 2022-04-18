def structure(x):
    """
    Crée la structure des joueurs
    :param: x: int Nombre de joueurs
    :return: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    """
    if x == 2:
        return [["bleu", 4, (1, 3), [], []], ["vert", 4, (27, 29), [], []]]

    colors = ["bleu", "rouge", "vert", "jaune"]
    players = []

    for tmp in range(x):
        players.append([colors[tmp], 4, (1 + (tmp * 13), 3 + (tmp * 13)), [], []])

    return players


def color_seperation(player, i):
    """
    Seperation des pieces en fonction de la couleur
    """
    if player[i][0] == "bleu":
        print(
            "\033[1;34m" + "====================================================================================" + "\033[0;0m")
    elif player[i][0] == "vert":
        print(
            "\033[1;32m" + "====================================================================================" + "\033[0;0m")
    elif player[i][0] == "rouge":
        print(
            "\033[1;31m" + "====================================================================================" + "\033[0;0m")
    elif player[i][0] == "jaune":
        print(
            "\033[1;33m" + "====================================================================================" + "\033[0;0m")


def ecrasement(player, i, item):
    """
    Ecrase une piece ennemie
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :param: case: int Case sur laquelle le joueur est
    """
    for j in range(0, len(player), 1):
        if j != i:
            if item in player[j][3]:
                player[j][3].remove(item)
                player[j][1] += 1

    return player


def sortir_piece(player, i):
    """
    Sort une piece de la maison du joueur i
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :return: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    """
    player[i][1] -= 1
    player[i][3].append(player[i][2][1])

    return ecrasement(player, i, player[i][2][1])


def move_homerun(player, i, dice, item=1, ia=False):
    """
    Déplace le joueur sur le homerun si indiqué puis le déplace du reste de dice
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :param: dice: int Nombre du dé
    :param: nb_player: int Nombre de joueurs
    """
    # Déplace la piece sur le homerun
    temp = item
    for y in range(dice):
        temp += 1
        if temp == 6:
            if not ia:
                print("Vous ne pouvez pas allez plus loin que la case 6")
            break

    player[i][4].append(temp)
    return player


def moove_plateau(player, i, dice, item, ia=False):
    """
    Déplace le joueur sur le plateau et vérifie si il est sur une piece ennemie (si oui alors il les supprimes)
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :param: dice: int Nombre du dé
    :param: nb_player: int Nombre de joueurs
    """
    temp = item
    while dice > 0:
        temp = (temp + 1) % 52
        dice -= 1
        if temp == (player[i][2][0] + 1):
            player[i][3].remove(item)
            for y in range(dice):
                temp += 1
                if temp == 6:
                    if not ia:
                        print("Vous ne pouvez pas allez plus loin que la case 6")
                    break
            player[i][4].append(temp)
            return player

    player[i][3].remove(item)
    player[i][3].append(temp)
    return ecrasement(player, i, temp)


def turn_piece(player, i):
    """
    Tour du joueur i
    :param player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param i: int Numero du joueur
    :return: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    """
    repeat = 0
    while True:
        if repeat == 3:
            print("Vous avez dépassé le nombre de tour autorisé")
            return player
        from random import randint
        dice = randint(1, 6)
        chose = "n"
        print(f"Le joueur {player[i][0]} a fait {dice}")

        if dice == 6:
            repeat += 1
            if player[i][1] != 0:
                chose = input("Vous pouvez sortir une piece (y/n) ? ")
            if chose == "y":
                return sortir_piece(player, i)

        if player[i][4] == [] and player[i][3] == []:
            return player

        if chose == "n" and player[i][4] != []:
            chose = input(f"Vous pouvez déplacer une piece du homerun {player[i][4]} (y/n) ? ")
            if chose == "y":
                item = int(input(f"Quelle piece voulez vous déplacer ? "))
                player = move_homerun(player, i, dice, item)
                if dice != 6:
                    break

        if chose == "n" and player[i][3] != []:
            chose = input(f"Vous pouvez déplacer une piece du plateau {player[i][3]}(y/n) ? ")
            if chose == "y":
                item = int(input(f"Quelle piece voulez vous déplacer ? "))
                player = moove_plateau(player, i, dice, item)
                if dice != 6:
                    break

    return player

def ia_turn_piece(player, i):
    """
    Tour du joueur i
    :param player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param i: int Numero du joueur
    :return: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    """
    repeat = 0
    while True:
        if repeat == 3:
            return player
        from random import randint
        dice = randint(1, 6)
        chose = "n"

        if dice == 6:
            repeat += 1
            if player[i][1] != 0:
                chose = "y"
            if chose == "y":
                return sortir_piece(player, i)

        if player[i][4] == [] and player[i][3] == []:
            return player

        if chose == "n" and player[i][4] != []:
            chose = "y"
            if chose == "y":
                item = max(player[i][4])
                player = move_homerun(player, i, dice, item, True)
                if dice != 6:
                    break

        if chose == "n" and player[i][3] != []:
            chose = "y"
            if chose == "y":
                item = max(player[i][3])
                player = moove_plateau(player, i, dice, item)
                if dice != 6:
                    break

    return player

def main_stat(player, number_games):
    """
    Affiche les statistiques des joueurs
    :param player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param number_games: int Nombre de parties
    """
    prob_win = [0] * len(player)
    tour_moyenne = 0
    win = 5
    for y in range(number_games):
        while True:
            for i in range(len(player)):
                tour_moyenne += 1
                player = ia_turn_piece(player, i)
                if player[i][4] == [6, 6, 6, 6]:
                    prob_win[i] += 1
                    win = i-1
                    break
                print(f"P{tour_moyenne}")
            if win != 5:
                break

    for i in prob_win:
        i = i / number_games
        print(f"Le joueur {i} a gagné {i * 100}% des parties")
    print(f"La moyenne de tour est de {tour_moyenne / number_games}")



if __name__ == "__main__":
    print("début de la Partie de Ludo")

    number_player = int(input("Vous voulez combien de joueurs (2-4) : "))

    print(f"Vous avez {number_player} joueurs en jeux",
          f"Début de la partie")

    player = structure(number_player)
    print(f"Informations des joueurs : {player}")

    stat = input("Voulez calculer les stats (y/n) ? ")
    if stat == "y":
        number_games = int(input("Combien de parties voulez vous jouer ? "))
        main_stat(player, number_games)

    win = 5
    if stat == "n":
        while True:
            for i in range(number_player):
                color_seperation(player, i)
                print(f"Tour du joueur {player[i][0]}")
                print(f"Informations du joueur {player[i][0]} : {player[i]}")
                player = turn_piece(player, i)
                print(f"Informations du joueur {player[i][0]} : {player[i]}")
                color_seperation(player, i)
                if player[i][4] == [6, 6, 6, 6]:
                    print("Le joueur a gagné")
                    win = i
                    break