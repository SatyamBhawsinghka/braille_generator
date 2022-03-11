# Translate alphabet based text to braille.
import pdb
import mapAlphaToBraille, mapBrailleToAlpha
import numpy as np

CAPITAL = chr(10272)  # ⠠
CAPITAL_DICT = '001000'
NUMBER = chr(10300)  # ⠼
NUMBER_DICT = '001111'
UNRECOGNIZED = '?'

# There is no braille symbol for a generic quote (").
# There is only open quotation (“) and closed quotation (”).
# Therefore we must keep track of what the last quotation was
# so that we may convert the generic quotation to a specific one.

# for etching I have used two " " instead of open/closed quotations to keep the process easier.
open_quotes = True


def extract_words(string):
    # Split up a sentence based on whitespace (" ") and new line ("\n") chars.
    words = string.split(" ")
    result = []
    n = 0
    for word in words:
        temp = word.split("\n")
        n += len(word)
        for item in temp:
            result.append(item)

    n += len(words)
    print(n, result)
    return n+1, result

def is_braille(char):
    # Return true if a char is braille.
    if len(char) > 1:
        return False
    return char in mapBrailleToAlpha.letters \
        or char in mapBrailleToAlpha.numbers \
        or char in mapBrailleToAlpha.punctuation \
        or char in mapBrailleToAlpha.contractions \
        or char == CAPITAL \
        or char == NUMBER

def trim(word):
    # Remove punctuation around a word. Example: cat." becomes cat
    while len(word) != 0 and not word[0].isalnum():
        word = word[1:]
    while len(word) != 0 and not word[-1].isalnum():
        word = word[:-1]
    return word

# word matrix -> 12*n
def numbers_handler(word, braille_mat, start_index):
    # Replace each group of numbers in a word to their respective braille representation.
    #print(start_index)
    if word == "":
        return braille_mat, word
    result = word[0]
    if word[0].isdigit():
        result = NUMBER + mapAlphaToBraille.numbers.get(word[0])
        braille_mat[start_index, :] = np.array(list(NUMBER_DICT + mapAlphaToBraille.code_table.get(word[0])))
        #print(braille_mat[start_index,:])
    for i in range(1, len(word)):
        if word[i].isdigit() and word[i-1].isdigit():
            result += mapAlphaToBraille.numbers.get(word[i])
            braille_mat[start_index+i,:] = np.array(list(mapAlphaToBraille.code_table.get(' ') + mapAlphaToBraille.code_table.get(word[i])))
            #print(braille_mat[start_index+i,:])
        elif word[i].isdigit():
            result += NUMBER + mapAlphaToBraille.numbers.get(word[i])
            braille_mat[start_index+i,:] = np.array(list(NUMBER_DICT + mapAlphaToBraille.code_table.get(word[i])))
            #print(braille_mat[start_index+i,:])
        else:
            result += word[i]
    return braille_mat, result

def capital_letters_handler(word, braille_mat, start_index):
    # Put the capital escape code before each capital letter.
    if word == "":
        return braille_mat, word
    result = ""
    index_j = 0
    for char in word:
        if char.isupper():
            result += CAPITAL + char.lower()
            # print(np.array(list(CAPITAL_DICT)))
            braille_mat[start_index + index_j, :6] = np.array(list(CAPITAL_DICT))
        else:
            result += char.lower()
        index_j += 1
    return braille_mat, result

def find_utf_code(char):
    # Find the UTF code of a particular character. Used what an unidentified char is found.
    if len(char) != 1:
        return -1
    for i in range(0, 55000):
        if char == chr(i):
            return i


def char_to_braille(char):
    # Convert an alphabetic char to braille.
    if is_braille(char):
        return char
    elif char == "\n":
        return "\n"
    elif char == "\"":
        global open_quotes
        if open_quotes:
            open_quotes = not open_quotes
            return mapAlphaToBraille.punctuation.get("“")
        else:
            open_quotes = not open_quotes
            return mapAlphaToBraille.punctuation.get("”")
    elif char in mapAlphaToBraille.letters and char.isupper():
        return CAPITAL + mapAlphaToBraille.letters.get(char)
    elif char in mapAlphaToBraille.letters:
        return mapAlphaToBraille.letters.get(char)
    elif char in mapAlphaToBraille.punctuation:
        return mapAlphaToBraille.punctuation.get(char)
    else:
        print("Unrecognized Symbol:", char, "with UTF code:", find_utf_code(char))
        return UNRECOGNIZED


def word_to_braille(word):
    # Convert an alphabetic word to braille.
    # if word in mapAlphaToBraille.contractions:
    #    return mapAlphaToBraille.contractions.get(word)
    #else:
    result = ""
    for char in word:
        result += char_to_braille(char)
    return result


def build_braille_word(trimmed_word, shavings, index, braille, word_, braille_mat, start_index):
    # Translate a trimmed word to braille then re-attach the shavings.
    if shavings == "":
        braille += word_to_braille(trimmed_word)
    else:
        for i in range(0, len(shavings)):
            if i == index and trimmed_word != "":
                braille += word_to_braille(trimmed_word)
            braille += word_to_braille(shavings[i])
        if index == len(shavings):  # If the shavings are all at the beginning.
            braille += word_to_braille(trimmed_word)
    i = 0
    #print(word_, start_index)
    for ch in word_:
        if is_braille(ch):
            continue
        else:
            braille_mat[start_index+i, 6:] = np.array(list(mapAlphaToBraille.code_table.get(ch)))
            #print(ch, start_index+i)
            i += 1
    #pdb.set_trace()

    return braille_mat, braille


def translate(string):
    # Convert alphabetic text to braille.
    braille = ""
    n, words = extract_words(string)
    braille_matrix = np.zeros((n+1,12))
    i_index = 0
    for word in words:
        # pdb.set_trace()
        # transform numbers to braille
        # replace the matrix with places with numbers
        braille_matrix, word = numbers_handler(word, braille_matrix, i_index)
        # add extrachracter of braille to denote cap letters
        # replace the 0to5 indices of the matrix to identify the capital_dict
        braille_matrix, word = capital_letters_handler(word, braille_matrix, i_index)
        
        trimmed_word = trim(word)  # Remove punctuation (ex: change dog?" to dog)
        untrimmed_word = word
        index = untrimmed_word.find(trimmed_word)
        #pdb.set_trace()
        # find punctuations
        shavings = untrimmed_word.replace(trimmed_word, "")

        # build braille word for alphabets and punctuations
        braille_matrix, braille = build_braille_word(trimmed_word, shavings, index, braille, word, braille_matrix, i_index)
        braille += " "
        
        # add a blank space after each word
        i_index += len(word)+1
        #print(i_index)
        braille_matrix[i_index, 6:] = np.array(list(mapAlphaToBraille.code_table.get(" ")))
        #i_index += 1
    # first matrix
    # second a string of braille chrs
    # transforming the above braille matrix to get a 3*n matrix which can be directly mapped in the camera frame
    # removing extra spaces from the end
    temp = braille_matrix[:-2,:]
    braille_matrix2 = []
    braille_matrix2.append([])
    #x[0].append([])
    #x[0][0].append(value1)
    for t in temp:
        # check if its a spacebar
        if np.all(t == 0):
            braille_matrix2.append([[0, 0], 
                            [0, 0],
                            [0, 0]])
        # check if its a numeric or a capital
        elif np.any(t[:5] != 0):
            braille_matrix2.append([[t[0], t[3]], 
                                [t[1], t[4]],
                                [t[2], t[5]]])
            braille_matrix2.append([[t[6], t[9]], 
                                [t[7], t[10]],
                                [t[8], t[11]]])
        else:
            braille_matrix2.append([[t[6], t[9]], 
                                [t[7], t[10]],
                                [t[8], t[11]]])
        
    return braille_matrix2, braille_matrix[:-2,:], braille[:-1]  # Remove the final space that was added.

    # 12 0 == " "
    # 6!=0 then numeric/caps; print that in braille
    # if first 6 zero -> alphabet 