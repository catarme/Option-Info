def param_player() -> tuple[int, int]:
    """
    Must choose the number of players and the number of AI,
    the name of the players is between 1 and 4 and the number of AI is the difference between the name of the player and the number 4
    :return: int, int
    """
    type_game: str = input("Do you want to play only with humans, with ia, or only with ia (0,1,2) : ")
    while type_game not in ["0", "1", "2"]:
        type_game = input("Do you want to play only with humans, with ia, or only with ia (0,1,2) : ")

    if type_game == "0":
        humain: int = int(input("Enter the number of human players (2 - 4): "))
        while humain < 2 or humain > 4:
            humain = int(input("Enter the number of human players (2 - 4): "))
        ia: int = 0

    elif type_game == "1":
        humain: int = int(input("Enter the number of human players (1 - 3): "))
        while humain < 1 or humain > 3:
            humain = int(input("Enter the number of human players (1 - 3): "))
        ia: int = int(input("Enter the number of ia players (0 - 2): "))
        while ia < 0 or ia > 2:
            ia = int(input("Enter the number of ia players (0 - 2): "))

    else:
        humain: int = 1
        ia: int = int(input("Enter the number of ia players (1 - 3): "))
        while ia < 1 or ia > 3:
            ia = int(input("Enter the number of ia players (1 - 3): "))

    return humain, ia


def load_data() -> tuple[int, int, int, list[int], int]:
    """
    Loads the game save in a .txt file with the structure :
    - nb_players_h
    - nb_players_ia
    - turn
    - position of the players like that 1 2 3 4 5
    - first player
    :return: int, int, int, list[int], int
    """
    name: str = input("Enter the name of the save file : ")
    from os import path as path
    while not path.isfile(name):
        name = input("Enter the name of the save file : ")

    with open(name, "r") as f:
        h: int = int(f.readline())
        nb_ia: int = int(f.readline())
        turn: int = int(f.readline())
        pos: list[int] = list(map(int, f.readline().split()))
        first: int = int(f.readline())

    return h, nb_ia, turn, pos, first


def save_data(h: int, nb_ia: int, pos: list[int], turns: int, first: int) -> None:
    """
    :param h  : int       : number of human players
    :param nb_ia : int       : number of ia players
    :param pos   : list[int] : position of the players like that 0 0 0 0
    :param turns : int       : number of turns
	:param first : int       : first player
    :return None
    """
    name: str = input("Enter the name of the save file : ")
    with open(name, "w") as f:
        f.write(str(h) + "\n")
        f.write(str(nb_ia) + "\n")
        f.write(str(turns) + "\n")
        f.write(" ".join(map(str, pos)) + "\n")
        f.write(str(first) + "\n")
    print("Game saved")


def index_error(L: list[int], index: int) -> int:
    """
    Renvoie le carractere à l'index de la liste L à l'index "index" si il dépasse la liste alors on recommence au début de la liste
    :param L : list[int] : liste de carracteres
    :param index : int : index de la liste
    :return : int : carractere à l'index de la liste L à l'index "index"
    """
    if index >= len(L):
        index = index - len(L)
    return L[index]


def main(h: int, nb_ia: int, pos: list[int], first: int, turn: int = 0) -> tuple[list[int], int]:
    """
    :param h     : int       : number of human players
    :param nb_ia    : int       : number of ia players
    :param pos      : list[int] : position of the players like that 0 0 0 0
	:param first    : int       : first player
    :param turn     : int = 0   : number of the player who is playing
    :return: list[int], int
    """
    while True:
        if turn == 0:
            temp_pos: int = index_error(pos, first)
        else:
            temp_pos: int = index_error(pos, turn)
        position: int = temp_pos
        if input("Do you want to save the game ? (y/n) : ") == "y":
            save_data(h, nb_ia, pos, turn, first)
            if input("Do you want to quit the game ? (y/n) : ") == "y":
                return pos, turn
        print(f"It's the turn of player {pos.index(position)}\n",
              f"The position of the players are : {position}\n",
              "Rolling the dice...")
        from random import randint
        dice: int = randint(1, 6)
        print(f"You rolled a {dice}")
        if position + dice > 100:
            position = 100 - (position + dice - 100)
        else:
            position += dice
        falls: list[int] = [1, 4, 9, 21, 28, 51, 71, 80]
        d_falls: list[int] = [38, 14, 31, 42, 84, 67, 91, 99]
        if position in falls:
            position = d_falls[falls.index(position)]
        snake: list[int] = [17, 54, 62, 64, 87, 93, 95, 98]
        d_snake: list[int] = [7, 19, 24, 34, 60, 73, 75, 79]
        if position in snake:
            position = d_snake[snake.index(position)]
        print(f"The position of the players are : {position}")

        pos[pos.index(temp_pos)] = position
        if position == 100:
            print(f"Player {pos.index(temp_pos)} won the game")
            return pos, turn
        first += 1
        turn += 1
        print("------------------------------------------------------")


if __name__ == "__main__":
    print("Jeu-Echelles")

    if input("Do you want to load a save ? (y/n) : ") == "y":
        nb_h, nb_ia, turn, pos, first = load_data()
    else:
        nb_h, nb_ia = param_player()
        pos: list[int] = [0] * (nb_h + nb_ia)
        from random import randint

        first: int = 0
        temp_first: list[int] = [0] * (nb_h + nb_ia)
        while temp_first.count(max(temp_first)) != 1:
            for i in range(nb_h + nb_ia):
                temp_first[i] = randint(0, 6)

        turn: int = 0

    print("Starting the game...")
    pos, turn = main(nb_h, nb_ia, pos, first, turn)

    print("\033[92m" + "------------------------------------------------------\n" + "\033[0m",
          "\033[92m" + "                  The game is over !                  \n" + "\033[0m",
          "\033[92m" + f"        The position of the players are : \n\t\t{pos}\n" + "\033[0m",
          "\033[92m" + f"        The number of the player who won is : {turn} \n" + "\033[0m",
          "\033[92m" + "------------------------------------------------------" + "\033[0m")

    # while True:
    #     for play in range(first, len(pos)):
    #         if input("Do you want to save the game ? (y/n) : ") == "y":
    #             save_data(h, nb_ia, pos, turn, first)
    #             if input("Do you want to quit the game ? (y/n) : ") == "y":
    #                 return pos, turn
    #
    #         print(f"It's the turn of player {play}\n",
    #               f"The position of the players are : {position}\n",
    #               "Rolling the dice...")
    #         from random import randint
    #         dice: int = randint(1, 6)
    #         print(f"You rolled a {dice}")
    #
    #         if position + dice > 100:
    #             position = 100 - (position + dice - 100)
    #         else:
    #             position += dice
    #
    #         falls: list[int] = [1, 4, 9, 21, 28, 51, 71, 80]
    #         d_falls: list[int] = [38, 14, 31, 42, 84, 67, 91, 99]
    #         if position in falls:
    #             position = d_falls[falls.index(position)]
    #
    #         snake: list[int] = [17, 54, 62, 64, 87, 93, 95, 98]
    #         d_snake: list[int] = [7, 19, 24, 34, 60, 73, 75, 79]
    #         if position in snake:
    #             position = d_snake[snake.index(position)]
    #
    #         print(f"The position of the players are : {position}")
    #         if play == 100:
    #             print(f"Player {(turn + 1) % (h + nb_ia)} won the game")
    #             return pos, turn
    #
    #         turn += 1
    #         print("------------------------------------------------------")
    #     first = 0
