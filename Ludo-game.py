# 4 pieces par joueurs (indéplacable une fois dans la poche de départ)
# 52 carrés (48 blancs)

# home run:
# 4 ensembles de 5 carrés
# apres 51 cases (jamais la 52), elle rentre dans le circuit du foyer (home run)


# partie (tant que toutes les pieces d'un joueur est dans la poche de départ):
# - nombre de joueurs (2-4)
# - couleurs (vert et bleu au début)
# - lancer de dé :
# 	- si 6:
# 		- Soit relancer et aditionner la somme des dés 
# 		- Soit sortir une pièce
# 	- si 3*6:
# 		- somme des dés remis à 0 et on relance
# 	- Appliquer à une seule piece
# - Si une piece attérit sur piece de meme couleurs:
# 	- Si le joueurs le veux et le peux (max 4):
# 		- Empilées les pieces et se déplaces comme si elles etaient une seule pieces (max 4) (elle ne peux etre renvoyer que par une pille de meme taille)

# Dans le home run :
# - elle avance exactement jusqu'à la poche de départ, sinon elle rebondit



from math import trunc


def rool_dice() -> int:
    """
    roll a die between 1 and 6
    """
    from random import randint
    return randint(1,6)

def games(players:dict, position:dict, player_turn:int, turn: int = 0) -> None:
    """
    Initialize the games
    """
    # for each player, we associate a value 0
    start_poche:list[int] = [0] * len(players)

    while True:
        print("Its the turn of player {}".format(player_turn))
        temp_dice:int = rool_dice()
        if temp_dice == 6:
            print("You got a 6, you can start")

            break
        print("The dice is {} you cant start the game".format(temp_dice))
        input()
        turn += 1


    # we initialize the position of the players
    while 4 not in start_poche:
    



if __name__ == "__main__":
    nb_player = int(input("How many players? "))
    while nb_player > 4 or nb_player < 2:
        nb_player = int(input("How many players? "))
    
    # Assign a color to each player (green and blue if 2)
    # like that {1: (0, [0])} avec le joueur : nombre de pion, positions des pions
    colors = ["green", "blue", "yellow", "red"]
    players = {}
    if nb_player == 2:
        players[colors[0]] = 0
        players[colors[1]] = 1
    else:
        for i in range(nb_player):
            players[colors[i]] = i
    
    # Initialize the games