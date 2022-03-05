
def load_ascii_art(file_name:str) -> str:
    """
    load a file containing the ASCII Art in an appropriate structure 
    """
    with open(file_name, 'r') as file:
        return file.read()

def save_ascii_art(file_name:str, ascii_art:str) -> None:
    """
    save the ASCII Art, contained in the chosen structure, in a text file
    """
    with open(file_name, 'w') as file:
        file.write(ascii_art)

def compress_ascii_art(ascii_art:str) -> str:
    """
    compress the ASCII Art by avoiding to store spaces 
    """
    ascii_art = ascii_art.replace(" ", "")
    return ascii_art

def decompress_ascii_art(ascii_art:str) -> str:
    """
    to ecompress an ASCII Art 
    """
    return ascii_art.replace("", " ")

def print_ascii_art(ascii_art:str) -> None:
    """
    display the ASCII Art on screen (i.e. in the terminal)
    """
    print(ascii_art)

def find_ascii_art_on_the_ascii_art(path, name) -> int:
    """
    search for the presence of an ASCII Art in another ASCII Art whose path/name is passed in parameter
    """
    ascii_art = load_ascii_art(path)
    ascii_art_to_find = load_ascii_art(name)
    ascii_art_to_find = compress_ascii_art(ascii_art_to_find)
    ascii_art = compress_ascii_art(ascii_art)
    return ascii_art.find(ascii_art_to_find)

def zoom_2_ascii_art(ascci_art:str) -> str:
    """
    We agree here that each character in the initial figure will be replaced by a square of four characters (2x2) having a value of 0.5. 
    character in the initial figure will be replaced by a square of four characters (2x2) with the same value 
    """
    ascii_art = ""
    for line in ascci_art.split("\n"):
        for char in line:
            ascii_art += char * 4
        ascii_art += "\n"
    return ascii_art

def same_ascii(ascci_art1:str, ascci_art2:str) -> bool:
    """
    compare two ASCII Art to see if they are identical
    """
    return ascci_art1 == ascci_art2

def inverse_ascii(ascci_art:str) -> str:
    """
    Invert the ASCII Art by replacing the blanks with the @ character and the other visible characters by a space
    """
    ascii_art = ""
    for line in ascci_art.split("\n"):
        for char in line:
            if char == " ":
                ascii_art += "@"
            else:
                ascii_art += " "
        ascii_art += "\n"
    return ascii_art

def symmetrical_figure(ascci_art:str) -> bool:
    """
    check if the current figure is symmetrical
    """
    ascii_art = inverse_ascii(ascci_art)
    return same_ascii(ascci_art, ascii_art)

def degree_rotation_180(ascci_art:str) -> str:
    """
    rotate the initial figure by 180 degrees
    """
    ascii_art = ""
    for line in ascci_art.split("\n")[::-1]:
        ascii_art += line + "\n"
    return ascii_art

def superimpose_ascii1_ascii2(ascci_art1:str, ascci_art2:str) -> str:
    """
    superimpose a new ASCII Art (A2) on the ASCII Art currently in memory (A1) according to the following strategy
    A1         |   A2       | Result
    Space      | Space      | Space
    Character  | Space      | Character
    Space      | Character  | Character
    Character1 | Character2 | Character2
    """
    ascii_art = ""
    for line1, line2 in zip(ascci_art1.split("\n"), ascci_art2.split("\n")):
        for char1, char2 in zip(line1, line2):
            if char1 == " " and char2 == " ":
                ascii_art += " "
            elif char1 == " " and char2 != " ":
                ascii_art += char2
            elif char1 != " " and char2 == " ":
                ascii_art += char1
            else:
                ascii_art += char2
        ascii_art += "\n"
    return ascii_art

if __name__ == "__main__":
    ascii = input("Enter the path of the ASCII Art you want to load: ")
    ascii_art = load_ascii_art(ascii)
    print(ascii_art)
    save_ascii_art("ascii_art.txt", ascii_art)
    ascii_art = load_ascii_art("ascii_art.txt")
    input()
    print(ascii_art)
    ascii_art = compress_ascii_art(ascii_art)
    print(ascii_art)
    input()
    ascii_art = decompress_ascii_art(ascii_art)
    print(ascii_art)
    input()
    ascii_art = zoom_2_ascii_art(ascii_art)
    print(ascii_art)
    input()
    ascii_art = inverse_ascii(ascii_art)
    print(ascii_art)
    input()
    ascii_art = degree_rotation_180(ascii_art)
    print(ascii_art)
    input()
    ascii_art = superimpose_ascii1_ascii2(ascii_art, ascii_art)
    print(ascii_art)
    input()