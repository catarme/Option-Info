def structure(x: int) -> list[list[str, int, tuple[int], list[int], list[int]]]:
    """
    Créer les variables de chaque joueur
    :param: x: int Nombre de joueurs
    :return: list: Caracteristiques de chaques joueurs
    """
    if x == 2:
        return [["bleu", 4, (1, 3), [], []], ["vert", 4, (27, 29), [], []]]

    colors = ["bleu", "rouge", "vert", "jaune"]
    players = []

    for tmp in range(x):
        players.append([colors[tmp], 4, (1 + (tmp * 13), 3 + (tmp * 13)), [], []])

    return players


def player_moove(info_player, liste, dice, nb_player, i) -> list[str, int, tuple[int], list[int], list[int]]:
    """
    Déplace les pieces sur le plateau et sur le homerun
    :param: dice: int: Valeur des dés
    :param: info_player: int: places des dés
    :return: list: Nouvelles caracteristiques de chaques joueurs
    """
    choose = input(f"Vous voulez déplacer quel pieces {info_player[i]} : ")
    while choose not in [str(tmp) for tmp in info_player[i][3]]:
        choose = input(f"Vous voulez déplacer quel pieces {info_player[i]} : ")

    temp_choose = liste[liste.index(int(choose))]
    while dice != 0:
        if temp_choose > info_player[2][0]:
            # Transfert des pieces vers le homerun
            info_player[i][3].remove(temp_choose)
            temp_choose = 1
            break
        else:
            temp_choose = (temp_choose + 1) % 52
            dice -= 1

    if dice != 0:
        if temp_choose == 6:
            # Associe la piece au homerun
            info_player[i][4].append(temp_choose)
            return info_player
        # Fait avancer les pieces
        temp_choose += 1

    # Vérifie si il n'est pas sur une piece énemie
    for j in range(0, nb_player, 1):
        if j != i:
            if temp_choose in info_player[i][3]:
                # Supprime la piece ennemie
                info_player[j][3].remove(temp_choose)
                info_player[j][1] += 1

    # Ajoute la piece au joueur
    info_player[i][3].append(temp_choose)
    return info_player


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

    while True:
        for i in range(number_player):
            print(f"C'est au tour du joueur {i}",
                  f"Vos infos. sont : {player[i]}")

            # Lance les dés (1 à 6)
            from random import randint

            dice = randint(1, 6)
            print(f"Vous avez fait {dice}")

            temp = player[i]

            if dice == 6 and temp[1] > 0:
                out = input("Voulez vous sortir une piece (o/n) : ")
                while out not in ["o", "n"]:
                    out = input("Entrée une valeur valide : ")

                if out == "o":
                    # Créer une liste de chaques pieces d'autres joueurs sur la case temp[2][1]
                    for j in range(0, number_player - 1, 1):
                        if j != i and player[2][1] in player[j][3]:
                            for tmp in player[j][3]:
                                if tmp == player[2][1]:
                                    player[j][3].remove(tmp)
                                    player[j][1] += 1
                    # Sort une piece
                    temp[1] -= 1
                    temp[3].append(temp[2][1])
                    continue

            moove = None
            if temp[4]:
                moove = input("Voulez vous déplacer une piece dans le homerun (o/n) : ")
                while moove not in ["o", "n"]:
                    moove = input("Entrée une valeur valide : ")

                if moove == "o":
                    player = player_moove(player, temp[4], dice, number_player, i)

            if temp[3] and moove is None:
                player = player_moove(player, temp[3], dice, number_player, i)

            if temp[4] and len(temp[4]) == 4:
                print(f"Le joueur {i} a gagné")
                break
