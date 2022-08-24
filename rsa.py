
import random
import numpy as np
import re

ASCII_list = np.array([['032', ' '], 
                        ['033' , '!'],
                        ['034' , '"'],
                        ['035' , '#'],
                        ['036' , '$'],
                        ['037' , '%'],
                        ['038' , '&'],
                        ['039' , "'"],
                        ['040' , '('],
                        ['041' , ')'],
                        ['042' , '*'],
                        ['043' , '+'],
                        ['044' , ','],
                        ['045' , '-'],
                        ['046' , '.'],
                        ['047' , '/'],
                        ['048' , '0'],
                        ['049' , '1'],
                        ['050' , '2'],
                        ['051' , '3'],
                        ['052' , '4'],
                        ['053' , '5'],
                        ['054' , '6'],
                        ['055' , '7'],
                        ['056' , '8'],
                        ['057' , '9'],
                        ['058' , ':'],
                        ['059' , ';'],
                        ['060' , '<'],
                        ['061' , '='],
                        ['062' , '>'],
                        ['063' , '?'],
                        ['064' , '@'],
                        ['065' , 'A'],
                        ['066' , 'B'],
                        ['067' , 'C'],
                        ['068' , 'D'],
                        ['069' , 'E'],
                        ['070' , 'F'],
                        ['071' , 'G'],
                        ['072' , 'H'],
                        ['073' , 'I'],
                        ['074' , 'K'],
                        ['075' , 'L'],
                        ['076' , 'M'],
                        ['077' , 'N'],
                        ['078' , 'O'],
                        ['079' , 'P'],
                        ['081' , 'Q'],
                        ['082' , 'R'],
                        ['083' , 'S'],
                        ['084' , 'T'],
                        ['085' , 'U'],
                        ['086' , 'V'],
                        ['087' , 'W'],
                        ['088' , 'X'],
                        ['089' , 'Y'],
                        ['090' , 'Z'],
                        ['091' , '['],
                        ['092' , '\\'],
                        ['093' , ']'],
                        ['094' , '^'],
                        ['095' , '_'],
                        ['096' , '`'],
                        ['097' , 'a'],
                        ['098' , 'b'],
                        ['099' , 'c'],
                        ['100' , 'd'],
                        ['101' , 'e'],
                        ['102' , 'f'],
                        ['103' , 'g'],
                        ['104' , 'h'],
                        ['105' , 'i'],
                        ['106' , 'j'],
                        ['107' , 'k'],
                        ['108' , 'l'],
                        ['109' , 'm'],
                        ['110' , 'n'],
                        ['111' , 'o'],
                        ['112' , 'p'],
                        ['113' , 'q'],
                        ['114' , 'r'],
                        ['115' , 's'],
                        ['116' , 't'],
                        ['117' , 'u'],
                        ['118' , 'v'],
                        ['119' , 'w'],
                        ['120' , 'x'],
                        ['121' , 'y'],
                        ['122' , 'z'],
                        ['123' , '{'],
                        ['124' , '|'],
                        ['125' , '}'],
                        ['126' , '~']])

def StringToASCII(string):
    array = list(string)
    ascii = ['1']
    for i in array:
        for j in range(94):
            if i == ASCII_list[j][1]:
                ascii.append(ASCII_list[j][0])
    number = ''
    for i in ascii:
        number += i
    return int(number)

def ASCIIToString(number):
    string = str(number)[1:]
    array = re.findall('...', string)
    characters = ['']
    for i in array:
        for j in range(94):
            if i == ASCII_list[j][0]:
                characters.append(ASCII_list[j][1])
    string = ''
    for i in characters:
        string += i
    return string

def GenPrivatePublicKeys():
    prime1 = GenerateProbablePrime(1000)
    prime2 = GenerateProbablePrime(1000)
    N = prime1 * prime2
    publickey = [N, 65537]
    d = DecryptionExponent(prime1, prime2, 65537)
    privatekey = [N, d]
    return privatekey, publickey

def GenerateProbablePrime(bits):
    x = False
    while x == False:
        n = RandomOddNumber(bits)
        if MillerRabin(n) == True:
            x = True 
        else:
            x = False
    return n

def RandomOddNumber(bits):
    N = [1] * bits
    for i in range(1, bits - 1):
        N[i] = random.randint(0,1)
    return BinaryDigitsToInteger(N)

def BinaryDigitsToInteger(N):
    n = 0
    pow2 = 1
    for i in reversed(range(len(N))):
        n += pow2 * N[i]
        pow2 *= 2
    return n

def MillerRabin(prime_candidate):
    if prime_candidate == 2:
        return True
    elif prime_candidate % 2 == 0:
        return False
    
    r, m = 0, prime_candidate - 1
    while m % 2 == 0:
        m //= 2
        r += 1
    for _ in range(10):
        a = random.randrange(2, prime_candidate - 1)
        x = pow(a, m, prime_candidate)
        if x == 1 or x == prime_candidate - 1:
            continue
        for _ in range(r):
            x = pow(x, 2, prime_candidate)
            if x == prime_candidate - 1:
                break
        else:
            return False
    return True 

def DecryptionExponent(prime1, prime2, e):
    phi = (prime1 - 1) * (prime2 - 1)
    d = ExtendedEuclidianAlgorithm(phi, e)
    return int(d)

def EuclideanAlgorithm(a, b):  #returns matrix
    matrix = np.array([[a, b, a // b, a % b]])
    i = 0
    while matrix[i, 3] != 0:
        c = matrix[i, 1]
        d = matrix[i, 3]
        row = [c, d, c // d, c % d]
        matrix = np.r_[matrix, [row]]
        i += 1
    return matrix

def ExtendedEuclidianAlgorithm(a, b):
    matrix = EuclideanAlgorithm(a, b)
    a_1 = 1
    a_2 = -1 * matrix[1, 2]
    b_1 = -1 * matrix[0, 2]
    b_2 = -1 * matrix[1, 2] * b_1 + 1
    for i in range(2, matrix.shape[0] - 1):
        a_3 = a_1 + (-1 * matrix[i, 2] * a_2)
        b_3 = b_1 + (-1 * matrix[i, 2] * b_2)
        a_1, a_2 = a_2, a_3
        b_1, b_2 = b_2, b_3
    return b_2

def EncryptMesage(message, e, N):
    encryptedmessage = pow(message, e, N)
    return encryptedmessage

def DecryptMessage(encryptedmessage, d, N):
    decryptedmessage = pow(encryptedmessage, d, N)
    return decryptedmessage

choice = input('encrypt or decrypt: ')

if choice == 'decrypt':
    privatekey, publickey = GenPrivatePublicKeys()
    print('N: ' + str(publickey[0]))
    print('encryption exponent: ' + str(publickey[1]))
    encryptedmessage = int(input('message to decrypt: '))
    asciimessage = DecryptMessage(encryptedmessage, privatekey[1], privatekey[0])
    print(ASCIIToString(asciimessage))
elif choice == 'encrypt':
    message = input('message to encrypt: ')
    asciimessage = StringToASCII(message)
    N = int(input('N: '))
    e = int(input('encryption exponent: '))
    print(EncryptMesage(asciimessage, e, N))
