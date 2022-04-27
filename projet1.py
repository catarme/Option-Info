from random import randint


def deplacement(positions: list[int], joueurs: int, de: int, echelles: list[tuple[int, int]], serpents: list[tuple[int, int]], fin: int) -> list[int]:
    """
    Déplace le pion d'un joueur
    :param positions: list[int]: liste des positions des joueurs
    :param joueurs: int: numero du joueur
    :param de: int: valeur du dé
    :param echelles: list[tuple[int, int]]: liste des cases d'entrée et de sortie des échelles
    :param serpents: list[tuple[int, int]]: liste des cases d'entrée et de sortie des serpents
    :param fin: int: case de fin de la partie
    :return: list[int]: liste des positions des joueurs après déplacement
    """
    if positions[joueurs] + de > fin:
        positions[joueurs] = fin - (positions[joueurs] + de - fin)
        return positions

    positions[joueurs] += de

    for temp in range(len(echelles)):
        if positions[joueurs] == echelles[temp][0]:
            positions[joueurs] = echelles[temp][1]
            return positions

    for temp in range(len(serpents)):
        if positions[joueurs] == serpents[temp][0]:
            positions[joueurs] = serpents[temp][1]
            return positions

    return positions


def main(nombre_humain: int, nombre_robot: int, echelles: list[tuple[int, int]], serpents: list[tuple[int, int]], fin: int, logs: bool=True, nombre_partie: int=1) -> None:
    """
    Fonction principale du jeu
    :param nombre_humain: int: nombre de joueurs humains
    :param nombre_robot: int: nombre de joueurs IA
    :param echelles: list[tuple[int, int]]: liste des cases d'entrée et de sortie des échelles
    :param serpents: list[tuple[int, int]]: liste des cases d'entrée et de sortie des serpents
    :param fin: int: case de fin de la partie
    :param logs: bool=True: affiche les logs de la partie si True
    :param nombre_partie: int=1: nombre de partie à jouer
    :return: None
    """
    nombre_joueurs = nombre_humain + nombre_robot
    winrate = [0] * nombre_joueurs
    positions = [0] * nombre_joueurs
    nombre_tour = 0

    for i in range(nombre_partie):
        fini = False
        while True:
            for temp in range(nombre_joueurs):
                nombre_tour += 1
                if temp <= nombre_humain and logs:
                    input("Appuyez pour lancer le dé")
                de = randint(1, 6)
                if logs:
                    print(f"Le joueur {temp} a fait {de}",
                          f"Vous etes sur la case {positions[temp]}")

                positions = deplacement(positions, temp, de, echelles, serpents, fin)

                if positions[temp] == fin:
                    if logs:
                        print(f"Le joueur {temp} a gagné")
                    winrate[temp] += 1
                    fini = True
                    break
            if fini:
                break

    if not logs:
        print(f"Le nombre de tour moyen par partie est de {nombre_tour / nombre_partie}")

        for temp in range(nombre_joueurs):
            print(f"Le joueur {temp+1} a gagné {winrate[temp] / nombre_partie * 100}% des parties")
    return


if __name__ == "__main__":
    fin = 100
    echelles: list[tuple[int, int]] = [(1, 38), (4, 14), (9, 31), (21, 42), (28, 84), (51, 67), (71, 91), (80, 99)]
    serpents: list[tuple[int, int]] = [(17, 7), (54, 19), (62, 24), (64, 34), (87, 60), (93, 73), (95, 75), (98, 79)]

    humain = int(input("Combien de joueurs humains (max 4) ? "))
    robot = int(input("Combien de joueurs robots (max 4) ? "))

    while (humain + robot) not in [2, 3, 4]:
        humain = int(input("Combien de joueurs humains (max 4) ? "))
        robot = int(input("Combien de joueurs robots (max 4) ? "))

    print("Début du jeu")

    if bool(input("Voulez-vous jouer faire des stats ? (y/n)") == 'y'):
        main(humain, robot, echelles, serpents, fin, logs=False, nombre_partie=int(input("Combien de parties ? ")))
    else:
        main(humain, robot, echelles, serpents, fin)
