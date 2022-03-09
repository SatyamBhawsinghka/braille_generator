# Contains dictionaries that map English letters to braille.

letters = {'a': chr(10241),
           'b': chr(10243),
           'c': chr(10249),
           'd': chr(10265),
           'e': chr(10257),
           'f': chr(10251),
           'g': chr(10267),
           'h': chr(10259),
           'i': chr(10250),
           'j': chr(10266),
           'k': chr(10245),
           'l': chr(10247),
           'm': chr(10253),
           'n': chr(10269),
           'o': chr(10261),
           'p': chr(10255),
           'q': chr(10271),
           'r': chr(10263),
           's': chr(10254),
           't': chr(10270),
           'u': chr(10277),
           'v': chr(10279),
           'w': chr(10298),
           'x': chr(10285),
           'y': chr(10301),
           'z': chr(10293)}

contractions = {'but': chr(10243),
                'can': chr(10249),
                'do': chr(10265),
                'every': chr(10257),
                'from': chr(10251),
                'go': chr(10267),
                'have': chr(10259),
                'just': chr(10266),
                'knowledge': chr(10280),
                'like': chr(10296),
                'more': chr(10253),
                'not': chr(10269),
                'people': chr(10255),
                'quite': chr(10271),
                'rather': chr(10263),
                'so': chr(10254),
                'that': chr(10270),
                'us': chr(10277),
                'very': chr(10279),
                'it': chr(10285),
                'you': chr(10301),
                'as': chr(10293),
                'and': chr(10287),
                'for': chr(10303),
                'of': chr(10295),
                'the': chr(10286),
                'with': chr(10302),
                'will': chr(10298),
                'his': chr(10278),
                'in': chr(10260),
                'was': chr(10292),
                'to': chr(10262)}

punctuation = {',': chr(10242),
               ';': chr(10246),
               ':': chr(10258),
               '.': chr(10290),
               '!': chr(10262),
               '(': chr(10294),
               ')': chr(10294),
               '“': chr(10278),
               '”': chr(10292),
               '?': chr(10278),
               '/': chr(10252),
               '#': chr(10300),
               '\'': chr(10244),
               '…': chr(10290) + chr(10290) + chr(10290),
               '’': chr(10244),
               '­': chr(10276),
               '-': chr(10276),
               '‐': chr(10276),
               '‑': chr(10276),
               '‒': chr(10276),
               '–': chr(10276),
               '—': chr(10276),
               '―': chr(10276)}

numbers = {'1': chr(10241),
           '2': chr(10243),
           '3': chr(10249),
           '4': chr(10265),
           '5': chr(10257),
           '6': chr(10251),
           '7': chr(10267),
           '8': chr(10259),
           '9': chr(10250),
           '0': chr(10266)}

# taken from https://stackoverflow.com/questions/41922629/convert-text-to-braille-unicode-in-python
# two columns placed next to each other
code_table = {
    'a': '100000',
    'b': '110000',
    'c': '100100',
    'd': '100110',
    'e': '100010',
    'f': '110100',
    'g': '110110',
    'h': '110010',
    'i': '010100',
    'j': '010110',
    'k': '101000',
    'l': '111000',
    'm': '101100',
    'n': '101110',
    'o': '101010',
    'p': '111100',
    'q': '111110',
    'r': '111010',
    's': '011100',
    't': '011110',
    'u': '101001',
    'v': '111001',
    'w': '010111',
    'x': '101101',
    'y': '101111',
    'z': '101011',
    '1': '100000',
    '2': '110000',
    '3': '100100',
    '4': '100110',
    '5': '100010',
    '6': '110100',
    '7': '110110',
    '8': '110010',
    '9': '010100',
    '0': '010110',
    ' ': '000000',
    ',': '000001',
    ';': '000011',
    ':': '100011',
    '.': '000101',
    '!': '011101',
    '(': '111011',
    ')': '011111',
    '“': '000010',
    '”': '000010',
    '?': '100111',
    '/': '001100',
    '#': '001111',
    '\'': '110011',
    '-': '001001',
    '―': '000111',
    '&': '111101',
    '$': '110101',
    '+': '001101',
    '*': '100001',
    '=': '111111'}