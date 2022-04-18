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


def ecrasement(player, i, case):
    """
    Ecrase une piece ennemie
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :param: case: int Case sur laquelle le joueur est
    """
    for j in range(0, len(player), 1):
        if j != i:
            if case in player[j][3]:
                player[j][3].remove(case)
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

    # vérifie si il n'est pas sur une piece énemie
    player = ecrasement(player, i, player[i][2][1])

    return player


def moove_homerun(player, i, dice, chose=1):
    """
    Déplace le joueur sur le homerun
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :param: dice: int Nombre du dé
    :param: nb_player: int Nombre de joueurs
    """
    temp = chose
    while True:
        temp += 1
        dice -= 1
        if temp == 6:
            print("Vous ne pouvez pas aller si loin")
            player[i][4].append(6)
            return player
        if dice == 0:
            break

    player[i][4].append(temp)

    return player


def moove_plateau(player, i, dice, chose):
    """
    Déplace le joueur sur le plateau et vérifie si il est sur une piece ennemie (si oui alors il les supprimes)
    :param: player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param: i: int Numero du joueur
    :param: dice: int Nombre du dé
    :param: nb_player: int Nombre de joueurs

    """
    temp = chose
    while True:
        temp = (temp + 1) % 52
        dice -= 1
        if temp == player[i][2][0] + 1:
            player[i][3].remove(chose)
            player = moove_homerun(player, i, dice)
            return player

        if dice == 0:
            break

    player[i][3].remove(chose)
    player[i][3].append(temp)

    player = ecrasement(player, i, chose)

    return player


def turn_piece(player, i):
    """
    Tour du joueur i
    :param player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param i: int Numero du joueur
    :return: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    """
    reapet = 0
    while True:
        from random import randint
        dice = randint(1, 6)
        chose = 'N'
        print(f"Le joueur {i} a lancé le dé et obtient              {dice}")

        if dice == 6:
            reapet += 1
            chose = input(f"Voulez vous sortir une piece sur la case {player[i][2][1]} ? (O/N)")
            if chose == "O":
                player = sortir_piece(player, i)
                break

        if chose == 'N':
            if player[i][3]:
                chose = input(f"Voulez vous déplacer une piece sur le parcours ? ({player[i][3]}/N)")
                if chose != "N" and int(chose) in player[i][3]:
                    player = moove_plateau(player, i, dice, int(chose))

            elif chose == "N" and player[i][4]:
                chose = input(f"Voulez vous déplacer une piece sur le homerun ? ({player[i][4]}/N)")
                if chose != "N" and int(chose) in player[i][4]:
                    player = moove_homerun(player, i, dice, int(chose))

        if reapet in [0, 3]:
            print("Vous ne pouvez jouer 3 fois d'affilé")
            return player

    return player


def close_plateau(player, i):
    """
    Calcule la piece dans player[i][3] qui est la plus proche de player[i][2][0]
    """
    temp = player[i][3]
    close = (52, 1)  # (piece, distance)
    distance = 0
    for piece in temp:
        while temp == player[i][2][0]:
            temp = (temp + 1) % 52
            distance += 1
        if distance < close[1]:
            close = (piece, distance)

        distance = 0

    return close[0]


def close_homerun(player, i, dice):
    """
    Calcule la piece dans player[i][4] qui a comme séparation le nombre de case le plus proche de la valeur de dice
    """
    temp = player[i][4]
    close = (52, 1)  # (piece, distance)
    dist = 0
    for piece in temp:
        # Calcul le reste de la soustractions entre la valeur de dice et la position de la piece jusqu'a la case 6
        dist = 6 - (piece + dice - 6)
        if dist > close[1]:
            close = (piece, dist)

        dist = 0

    return close[0]


def ia_turn(player, i):
    """
    Fait jouer une IA qui répond en prioriter la sortie de piece et en second temps le déplacement de la piece la moins éloignée de la case player[i][2][0]
    :param player: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    :param i: int Numero du joueur
    :return: list[list[str, int, tuple[int], list[int], list[int]]] Liste des joueurs
    """
    reapet = 0
    while True:
        from random import randint
        if reapet == 4:
            print("Vous ne pouvez jouer 3 fois d'affilé")
            break
        dice = randint(1, 6)
        chose = 'N'

        if dice == 6:
            if player[i][3] or player[i][4]:
                chose = "N"
            else:
                chose = "O"
            if chose == "O":
                player = sortir_piece(player, i)
                break

        if chose == 'N' and player[i][4]:
            player = moove_homerun(player, i, dice, close_homerun(player, i, dice))
            continue

        elif chose == "N" and player[i][3]:
            player = moove_plateau(player, i, dice, close_plateau(player, i))
            continue

        if reapet == 3:
            print("Vous ne pouvez jouer 3 fois d'affilé")
            break

    return player


def statistics(player, nb_games):
    """
    Calcule les statistiques de chaque joueur (nombre de victoire, nombre de défaite, nombre de tours joués)
    """
    prob_win = [0] * len(player)
    prob_loose = [0] * len(player)
    prob_tour = [0] * len(player)
    for y in range(nb_games):
        while True:
            for i in range(number_player):
                player = ia_turn(player, i)

                prob_tour[i] += 1

                if player[i][4] == [6, 6, 6, 6]:
                    print("L'IA a gagné")
                    prob_win[i] += 1
                    break
            break
        prob_win[i] += 1

    for i in range(len(player)):
        color_seperation(player, i)
        print(f"Le joueur {i} a gagné {prob_win[i]} fois sur {nb_games} parties")
        print(f"Le joueur {i} a perdu {prob_loose[i]} fois sur {nb_games} parties")
        print(f"Le joueur {i} a joué {prob_tour[i]} fois sur {nb_games} parties")
        color_seperation(player, i)


if __name__ == "__main__":
    print("début de la Partie de Ludo")

    number_player = input("Vous voulez combien de joueurs (2-4) : ")
    while number_player not in ['2', '3', '4']:
        number_player = input("Entrée une valeur valide : ")

    number_player = int(number_player)
    print(f"Vous avez {number_player} joueurs en jeux",
          f"Début de la partie")

    player = structure(number_player)
    print(f"Informations des joueurs : {player}")

    stat = input("Voulez vous faire des statistiques ? (O/N)")
    if stat == "O":
        stat = True
        nb_game = int(input("Combien de parties voulez vous faire ? "))
        print("")
        statistics(player, nb_game)

    else:
        while True:
            for i in range(number_player):
                color_seperation(player, i)
                print(f"C'est au tour du joueur {i}",
                      f"Vos infos. sont : {player[i]}")

                player = turn_piece(player, i)

                print(f"Vos infos. sont : {player[i]}")

                color_seperation(player, i)

                if player[i][4] == [6, 6, 6, 6]:
                    print(f"Le joueur {player[i][0]} a gagné")
                    print(f"Le score du joueur {player[i][0]} est de {player[i][1]}")

                    for j in range(len(player)):
                        if j != i:
                            print(f"Le score du joueur {player[j][0]} est de {player[j][1]}")
                    break
