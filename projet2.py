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
    Déplacement d'une pièce du homerun
    :param joueurs: list: liste des joueurs
    :param numero_joueur: int: numéro du joueur
    :param pieces: int: numéro de la pièce
    :param de: int: valeur du dé
    :return: list: liste des joueurs avec les modifications
    """
    temp = pieces + de if pieces + de <= 6 else 6

    joueurs[numero_joueur][4].remove(pieces)
    joueurs[numero_joueur][4].append(temp)

    return joueurs


def sortir_piece(joueurs: list[list[str, int, tuple[int], list[int], list[int]]], numero_joueur: int,
                 case_sortie: int) -> list[list[str, int, tuple[int], list[int], list[int]]]:
    """
    Fait sortir une pièce du plateau sur la case de sortie
    :param joueurs: list: liste des joueurs
    :param numero_joueur: int: numéro du joueur
    :param case_sortie: int: case de sortie
    :return: list: liste des joueurs avec les modifications
    """
    joueurs[numero_joueur][1] -= 1
    joueurs[numero_joueur][3].append(case_sortie)

    for temp in range(len(joueurs)):
        if numero_joueur == temp or case_sortie not in joueurs[temp][3]:
            continue
        joueurs[temp][3].remove(case_sortie)
        joueurs[temp][1] += 1

    return joueurs


def deplacement_plateau(joueurs: list[list[str, int, tuple[int], list[int], list[int]]], numero_joueur: int,
                        pieces: int, de: int):
    """
    Deplacément d'une pièce du plateau
    :param joueurs: list: liste des joueurs
    :param numero_joueur: int: numéro du joueur
    :param pieces: int: numéro de la pièce
    :param de: int: valeur du dé
    :return: list: liste des joueurs avec les modifications
    """
    if ((pieces + de) % 52) >= (joueurs[numero_joueur][2][0] + 1):
        temps = pieces
        while de:
            temps += 1
            de -= 1
            if (temps % 52) == joueurs[numero_joueur][2][0] + 1:
                joueurs[numero_joueur][3].remove(pieces)
                joueurs[numero_joueur][4].append(1 + de)
                return joueurs

    else:
        temps = ((pieces + de) % 52)

    for temp in range(len(joueurs)):
        if numero_joueur == temp or temp not in joueurs[temp][3]:
            continue
        joueurs[temp][3].remove(temp)
        joueurs[temp][1] += 1

    joueurs[numero_joueur][3].remove(pieces)
    joueurs[numero_joueur][3].append(temps)

    return joueurs


def deplacement(joueurs: list[list[str, int, tuple[int], list[int], list[int]]], tour: int, robot: bool = False):
    """
    Assure le respect des règles pour chaque coup
    :param joueurs: list: liste des joueurs
    :param tour: int: numéro du tour
    :param robot: bool: si le joueur est un robot
    :return: list: liste des joueurs avec les modifications
    """
    from random import randint
    for i in range(3):
        de = randint(1, 6)
        chose = "n"
        if not robot:
            print(f"Le joueur {joueurs[tour][0]} a obtenu {de}")

        if de == 6 and joueurs[tour][1] > 0:
            if not robot:
                chose = input("Souhaitez-vous sortir une pièce (y/n) ? ")
            else:
                chose = "y"
            if chose == "y":
                joueurs = sortir_piece(joueurs, tour, joueurs[tour][2][1])

        if len(joueurs[tour][3]) + len(joueurs[tour][4]) == 0:
            return joueurs

        if chose != "y" and len(joueurs[tour][4]) > 0 and joueurs[tour][4] != [6] * len(joueurs[tour][4]):
            if not robot:
                chose = input("Souhaitez-vous déplacer une piece dans la maison (y/n) ? ")
            else:
                chose = "y"

            if chose == "y":
                if not robot:
                    piece = int(input(f"Quelle pièce voulez-vous déplacer {joueurs[tour][4]} ? "))
                else:
                    piece = random.choice(joueurs[tour][4])

                joueurs = deplacement_homerun(joueurs, tour, piece, de)
                if de != 6:
                    return joueurs

        if chose != "y" and len(joueurs[tour][3]) > 0:
            if not robot:
                chose = input("Souhaitez-vous déplacer une pièce du plateau (y/n) ? ")
            else:
                chose = "y"

            if chose == "y":
                if not robot:
                    piece = int(input(f"Quelle pièce voulez-vous déplacer {joueurs[tour][3]} ? "))
                else:
                    piece = random.choice(joueurs[tour][3])

                joueurs = deplacement_plateau(joueurs, tour, piece, de)
                if de != 6:
                    return joueurs
    return joueurs


def main(humain: int, robot: int) -> str:
    """
    Exécute la partie
    :param robot: int: nombre d'IA
    :param humain: int: nombre de joueur humain
    :return: str: couleur du gagnant
    """
    nb_joueur = humain + robot
    joueurs = structure(nb_joueur)
    tours = 0

    while True:
        for tour in range(nb_joueur):
            tours += 1
            print(f"C'est au tour de {joueurs[tour][0]}")
            if tour < humain:
                joueurs = deplacement(joueurs, tour)
            else:
                joueurs = deplacement(joueurs, tour, True)
            print(joueurs)
            # Regarde si le joueur a gagné
            if joueurs[tour][4] == [6, 6, 6, 6]:
                print(f"Le joueur {joueurs[tour][0]} a gagné",
                      f"Il y a eu {tours} tours")
                return joueurs[tour][0]


def main_statistique(nombre_robot: int, nombre_partie: int) -> None:
    """
    Exécute nombre_partie de ludo game
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
                if joueurs[tour][4] == [6, 6, 6, 6]:
                    winrate[tour] += 1
                    fini = True
                    break

            nb_tour += 1
            if fini:
                break

    for temp in range(nombre_robot):
        print(f"Le joueur {temp} a gagné {winrate[temp] / nombre_partie * 100}% des parties")

    return


if __name__ == '__main__':
    humain = int(input("Nombre de joueurs humains: (max 4) : "))
    robot = int(input(f"Nombre de joueurs robots: (max 4) : "))

    while (humain + robot) not in [2, 3, 4]:
        humain = int(input("Nombre de joueurs humains: (max 4) : "))
        robot = int(input(f"Nombre de joueurs robots: (max 4) : "))

    print("\n")
    print(f"Humain: {humain}")
    print(f"Robot: {robot}")
    print("\n")

    statistique = input("Souhaitez-vous afficher les statistiques? (y/n) : ")

    if statistique == "y":
        nombre_partie = int(input("Nombre de parties: "))
        main_statistique(humain, nombre_partie)

    else:
        gagnant = main(humain)
        print(f"Le gagnant est le joueur {gagnant}")
