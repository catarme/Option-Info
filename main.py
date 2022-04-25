import random


def structure(nombre_joueur: int) -> list[list[str, int, tuple[int], list[int], list[int]]]:
    """
    Structure de la partie
    :param nombre_joueur: int: nombre de joueurs
    :return: list: liste des joueurs
    """
    if nombre_joueur == 2:
        return [["bleu", 4, (1, 3), [], []], ["vert", 4, (27, 29), [], []]]

    couleurs = ["bleu", "rouge", "vert", "jaune"]
    joueurs: list[list[str, int, tuple[int], list[int], list[int]]] = []

    for temp in range(nombre_joueur):
        joueurs.append([couleurs[temp], 4, (1 + (temp * 13), 3 + (temp * 13)), [], []])

    return joueurs


def deplacement_homerun(joueurs: list, numero_joueur: int, pieces: int, de: int):
    """
    Deplacement d'une piece du homerun
    :param joueurs: list: liste des joueurs
    :param numero_joueur: int: numero du joueur
    :param pieces: int: numero de la piece
    :param de: int: nombre du dé
    :return: list: liste des joueurs avec les modifications
    """
    temp = pieces + de if pieces + de <= 6 else 6

    joueurs[numero_joueur][4].remove(pieces)
    joueurs[numero_joueur][4].append(temp)

    return joueurs


def sortir_piece(joueurs: list[list[str, int, tuple[int], list[int], list[int]]], numero_joueur: int, case_sortie: int):
    """
    Fait sortir une piece du plateau sur la case de sortie
    :param joueurs: list: liste des joueurs
    :param numero_joueur: int: numero du joueur
    :param case_sortie: int: case de sortie
    :return: list: liste des joueurs avec les modifications
    """
    joueurs[numero_joueur][1] -= 1
    joueurs[numero_joueur][3].append(case_sortie)

    for temp in range(len(joueurs)):
        if numero_joueur != temp and case_sortie in joueurs[temp][3]:
            joueurs[temp][3].remove(case_sortie)
            joueurs[temp][1] += 1

    return joueurs


def deplacement_plateau(joueurs: list[list[str, int, tuple[int], list[int], list[int]]], numero_joueur: int, pieces: int, de: int):
    """
    Deplacement d'une piece du plateau
    :param joueurs: list: liste des joueurs
    :param numero_joueur: int: numero du joueur
    :param pieces: int: numero de la piece
    :param de: int: nombre du dé
    :return: list: liste des joueurs avec les modifications
    """
    if ((pieces + de) % 52) >= (joueurs[numero_joueur][2][0] + 1):
        temps = pieces
        while de:
            temps += 1
            de -= 1
            if (temps % 52) == joueurs[numero_joueur][2][0] + 1:
                # Supprime la piece du plateau
                joueurs[numero_joueur][3].remove(pieces)
                # Ajoute la piece au homerun
                joueurs[numero_joueur][4].append(1 + de)
                return joueurs

    else:
        temps = ((pieces + de) % 52)

    # Supprime les pieces ennemies sur cette case
    for temp in range(len(joueurs)):
        if numero_joueur != temp and temp in joueurs[temp][3]:
            joueurs[temp][3].remove(temp)
            joueurs[temp][1] += 1

    # Regarde si la piece est sur la case d'entrée

    joueurs[numero_joueur][3].remove(pieces)
    joueurs[numero_joueur][3].append(temps)

    return joueurs


def deplacement(joueurs: list[list[str, int, tuple[int], list[int], list[int]]], tour: int, robot: bool = False):
    """
    Assure le respet des regles dans un tour de joueur
    :param joueurs: list: liste des joueurs
    :param tour: int: numero du tour
    :param robot: bool: si le joueur est un robot
    :return: list: liste des joueurs avec les modifications
    """
    from random import randint
    for temp in range(3):
        de = randint(1, 6)
        chose = "n"
        if not robot:
            print(f"Le joueur {joueurs[tour][0]} a fait {de}")

        # Si le joueur a fait un 6 et que ce n'est pas un robot alors on lui demande si il veut sortir une piece
        if de == 6 and joueurs[tour][1] > 0:
            if not robot:
                chose = input("Vous pouvez sortir une piece (y/n) ? ")
            else:
                chose = "y"
            if chose == "y":
                joueurs = sortir_piece(joueurs, tour, joueurs[tour][2][1])

        if len(joueurs[tour][3]) + len(joueurs[tour][4]) == 0:
            return joueurs

        # Si il a deja une piece sur la maison alors on lui demande il veut la déplacer
        # regarde si tout les valeur de joueurs[tour][4] sont égale à 6

        if chose != "y" and len(joueurs[tour][4]) > 0 and joueurs[tour][4] != [6] * len(joueurs[tour][4]):
            if not robot:
                chose = input("Vous pouvez déplacer une piece dans la maison (y/n) ? ")
            else:
                chose = "y"

            if chose == "y":
                # Demande quel piece il veut déplacer
                if not robot:
                    piece = int(input(f"Quelle piece voulez vous déplacer {joueurs[tour][4]} ? "))
                else:
                    piece = random.choice(joueurs[tour][4])

                joueurs = deplacement_homerun(joueurs, tour, piece, de)
                if de != 6:
                    return joueurs

        if chose != "y" and len(joueurs[tour][3]) > 0:
            if not robot:
                chose = input("Vous pouvez déplacer une piece du plateau (y/n) ? ")
            else:
                chose = "y"

            if chose == "y":
                # Demande quel piece il veut déplacer
                if not robot:
                    piece = int(input(f"Quelle piece voulez vous déplacer {joueurs[tour][3]} ? "))
                else:
                    piece = random.choice(joueurs[tour][3])

                joueurs = deplacement_plateau(joueurs, tour, piece, de)
                if de != 6:
                    return joueurs
    return joueurs


def main(humain: int) -> str:
    """
    Execute une partie de jeux normal
    :param humain: int: nombre de joueur humain
    :return: None
    """
    nb_joueur = humain
    joueurs = structure(nb_joueur)
    tours = 0

    while True:
        for tour in range(nb_joueur):
            tours += 1
            print(f"C'est au tour de {joueurs[tour][0]}")
            joueurs = deplacement(joueurs, tour)
            print(joueurs)
            # Regarde si le joueur a gagné
            if joueurs[tour][4] == [6, 6, 6, 6]:
                print(f"Le joueur {joueurs[tour][0]} a gagné",
                      f"Il y a eu {tours} tours")
                return joueurs[tour][0]


def main_statistique(nombre_robot: int, nombre_partie: int) -> None:
    """
    Execute nombre_partie de ludo game
    :param nombre_robot: int: nombre de robot
    :param nombre_partie: int: nombre de partie
    :return: None
    """
    nb_tour = 0
    winrate = [0] * nombre_robot

    for temp in range(nombre_partie):
        joueurs = structure(nombre_robot)
        fini = False
        while True:
            for tour in range(nombre_robot):
                joueurs = deplacement(joueurs, tour, True)
                # print(joueurs)
                if joueurs[tour][4] == [6, 6, 6, 6]:
                    winrate[tour] += 1
                    fini = True
                    break

            nb_tour += 1
            if fini:
                break

    for temp in range(nombre_robot):
        # Affiche le % de victoire
        print(f"Le joueur {temp} a gagné {winrate[temp] / nombre_partie * 100}% des parties")


if __name__ == '__main__':
    humain = int(input("Nombre de joueur humain: (1-4) : "))
    # robot = int(input(f"Nombre de joueur robot: (1-4) : "))

    while humain not in [2, 3, 4]:
        humain = int(input("Nombre de joueur humain: (1-4) : "))
        # robot = int(input(f"Nombre de joueur robot: (1-4) : "))

    print("\n")
    print(f"Humain: {humain}")
    # print(f"Robot: {robot}")
    print("\n")

    statistique = input("Voulez vous afficher les statistiques? (y/n) : ")
    if statistique == "y":
        nombre_partie = int(input("Nombre de partie: "))
        main_statistique(humain, nombre_partie)

    else:
        gagnant = main(humain)
        print(f"Le gagnant est le joueur {gagnant}")
