# Access point for translating braille to text and vice verse.
import printer, alphaToBraille2
from sys import argv

def menu():
    print('''
    Usage:
        main2.py <parameter>
        main2.py <file name> <parameter>
    Parameters:
        --text    | -t      translate text to braille
        --help    | -h      display this screen
        --map     | -m      print translation map
    ''')

def user_text():
    print("Input Text: ", end="")
    # first matrix
    # second a string of braille chrs
    braille_results = alphaToBraille2.translate(input())
    print(braille_results[0])
    #print(braille_results[1])

def open_text(filename):
    file = open(filename)
    content = file.read()
    # first matrix
    # second a string of braille chrs
    braille_results = alphaToBraille2.translate(content)
    print("Printing each character one after the other for ease in understanding!")
    print('The n*3*2 matrix represents n - characters which must be spaced equally irrespective of their type.\nThe type conversions are already done, the spacebars are alread taken care of.')
    print('All 3*2 = 0s represent space, which automatically is printed(not) on the paper')
    for arr in braille_results[0]:
        if arr != []:
            print(arr[0])
            print(arr[1])
            print(arr[2])
            print()
    #print(braille_results[0])
    #print(braille_results[1])

def argument_handler():
    if len(argv) == 1:
        menu()
    elif len(argv) == 2:
        # to tell the system thet it needs to convert text to braille
        if argv[1] == "--text" or argv[1] == "-t":
            user_text()
        elif argv[1] == "--map" or argv[1] == "-m":
            printer.all_braille()
        else:
            menu()
    elif len(argv) == 3:
        print(argv[0], argv[1], argv[2])
        # to open the textfile
        if argv[2] == "--text" or argv[2] == "-t":
            open_text(argv[1])
        elif argv[2] == "--map" or argv[2] == "-m":
            printer.all_braille()
        else:
            menu()
    else:
        menu()


if __name__ == "__main__":
    # input a filename and "--text" as arguments
    argument_handler()
