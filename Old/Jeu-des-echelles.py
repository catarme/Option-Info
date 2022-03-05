from random import randint

def chose_player() -> tuple[int, int]:
    """
    Must choose the number of players and the number of AI, 
    the name of the players is between 1 and 4 and the number of AI is the difference between the name of the player and the number 4
    """
    player: int = 0
    ia: int = 0
    bool_ia: int = int(input("Do you want to play only with humans, with ia, or only with ia (0,1,2) : "))
    while bool_ia > 2 or bool_ia < 0:
        bool_ia = int(input("Please enter a valid number : "))
    if bool_ia == 0:
        while player < 2 or player > 4:
            player = int(input("How many players are there? (1-4)"))
        ia = 0
    elif bool_ia == 1:
        while player < 2 or player > 3:
            player = int(input("How many players are there? (2-3)"))
        ia = abs(player - 4)
    elif bool_ia == 2:
        player = 1
        ia = 3
    return player, ia


def first_player_index(player: int) -> int:
    """
    Ask each player to roll a die, if there is no tie (if not, start over) then the player with the highest number starts the game 
    """
    L: list[int] = []
    while L.count(max(L)) != 1:
        for i in range(player):
            L.append(randint(1, 6))
    return L.index(max(L))


def load_game_save() -> tuple[int, int, int, list[int], int]:
    """
    Loads the game save in a .txt file with the structure :
    - nb_players_h
    - nb_players_ia
    - turn
    - position of the players like that 1 2 3 4 5
    - first player
    """
    name: str = input("What is the name of the file? (without the extension): ")
    import os
    while not os.path.isfile(f"{name}.txt"):
        name = input("This file does not exist, please enter a valid file name : ")
    # import Union
    from typing import Union
    with open(f"{name}.txt", "r") as file:
        turn: int = int(file.readline())
        pos: list[Union[str, int]] = file.readline().split()
        p_turn: int = int(file.readline())
        play_h: int = int(file.readline())
        play_ia: int = int(file.readline())

    pos = [int(i) for i in position]
    return play_h, play_ia, turn, pos, p_turn


def save_game(nb_players_h: int, nb_players_ia: int, turn: int, positon: list[int], player_turn: int) -> None:
    """
    save the game save in a .txt file with the structure :
    - nb_players_h
    - nb_players_ia
    - turn
    - position of the players
    - first player
    """
    name = input("What is the name of the file? (without the extension): ")
    with open(f"{name}.txt", "w") as file:
        file.write(f"{turn}\n")
        file.write(f"{' '.join(str(i) for i in positon)}\n")
        file.write(f"{player_turn}\n")
        file.write(f"{nb_players_h}\n")
        file.write(f"{nb_players_ia}\n")
    print("Game saved")


def main(nb_players_h: int, nb_players_ia: int, turn: int, position: list[int], player_turn: int) -> tuple[int, list[int], int, int, int]:
    """
    The main function of the game, it is called when the game is started
    """
    # if turn == 0:
    #     position = [0] * (nb_players_h + nb_players_ia)

    while 100 not in position:
        print(f"It is the turn of player {player_turn}")
        print(f"The position of the players are : {position[player_turn]}")
        print("Rolling the dice", end="")

        dice = randint(1, 6)
        print(f"\nYou rolled a {dice}")
        if position[player_turn] + dice > 100:
            position[player_turn] = 100 - (position[player_turn] + dice - 100)
        else:
            position[player_turn] += dice
        falls = [1, 4, 9, 21, 28, 51, 71, 80]
        for i in falls:
            if position[player_turn] == i:
                destination = [38, 14, 31, 42, 84, 67, 91, 99]
                print("You are on a ladder")
                position[player_turn] = destination[falls.index(i)]

        snake = [17, 54, 62, 64, 87, 93, 95, 98]
        for i in snake:
            if position[player_turn] == i:
                destination = [7, 19, 24, 34, 60, 73, 75, 79]
                print("You are on a snake")
                position[player_turn] = destination[snake.index(i)]

        print(f"You are now on square {position[player_turn]}")
        if position[player_turn] == 100:
            print("You win!")
            return turn, position, player_turn, nb_players_h, nb_players_ia

        player_turn = (player_turn + 1) % (nb_players_h + nb_players_ia)
        print("------------------------------------------------------")
        turn += 1
        save: str = input("Do you want to save the game? (y/n): ")
        if save == "y":
            save_game(nb_players_h, nb_players_ia, turn, position, player_turn)
            quit: str = input("Do you want to quit the game? (y/n): ")
            if quit == "y":
                return turn, position, player_turn, nb_players_h, nb_players_ia


def ia_game(number_ia: int) -> tuple[int, int]:
    """
    The function that is called when the game is played with ia
    """
    position = [1] * number_ia
    turn = 0
    turn_players = 0
    while 100 not in position:
        turn_players = turn % number_ia
        dice = randint(1, 6)

        if position[turn_players] + dice > 100:
            position[turn_players] = 100 - (position[turn % number_ia] + dice - 100)
        else:
            position[turn_players] += dice

        falls = [1, 4, 9, 21, 28, 51, 71, 80]
        for i in falls:
            if position[turn_players] == i:
                destination = [38, 14, 31, 42, 84, 67, 91, 99]
                position[turn_players] = destination[falls.index(i)]
        snake = [17, 54, 62, 64, 87, 93, 95, 98]
        for i in snake:
            if position[turn_players] == i:
                destination = [7, 19, 24, 34, 60, 73, 75, 79]
                position[turn % number_ia] = destination[snake.index(i)]
        if position[turn_players] == 100:
            return turn_players, turn
        turn += 1


if __name__ == '__main__':
    nb_players_h: int = 0
    nb_players_ia: int = 0
    turn: int = 0
    player_turn: int = 0
    position: list[int] = []

    load: str = input("Do you want to load a game? (y/n): ")

    if load == "y":
        nb_players_h, nb_players_ia, turn, position, player_turn = load_game_save()
        position = [int(i) for i in position]

    else:
        nb_players_h, nb_players_ia = chose_player()
        turn = 0
        position = [0] * (nb_players_h + nb_players_ia)
    if nb_players_h != 1:
        first_player = first_player_index(nb_players_h)
    else:
        first_player = 0
    turn, position, player_turn, nb_players_h, nb_players_ia = main(nb_players_h, nb_players_ia, turn, position,
                                                                    first_player)

    print("------------------------------------------------------")
    print("The game is over")
    print("The position of the players are : {}".format(position))
    print("The winner is player {}".format(turn % (nb_players_h + nb_players_ia)))
    print("The number of turns is {}".format(turn))
    print("           of players is {}".format(nb_players_h + nb_players_ia))
    print("           of human players is {}".format(nb_players_h))
    print("           of ia players is {}".format(nb_players_ia))
