message = input("What would you like to encrypt (default: '0123456789ABCDEF' ): ") or '0123456789ABCDEF'
key = input("What is the key (default: '133457799BBCDFF1'): ") or '133457799BBCDFF1'

message = message.upper()
key = key.upper()

########################################## BEGIN INPUT MANIPULATION ##########################################
def converthex(c):
    return ''.join(['{0:04b}'.format(int(x, 16)) for x in c])

#print(converthex("9"))
#print(converthex("A"))
#print(converthex("F"))

def convertbinary(binary_str):
    decimal_value = int(binary_str, 2)
    hex_value = hex(decimal_value)[2:].upper()  # Remove the '0x' prefix and convert to uppercase
    return hex_value

#print(convertbinary("0010"))
#print(convertbinary("1111"))

# Convert binary to decimal
def conBtodec(binary):
    decimal = 0
    base = 1

    while binary > 0:
        last = binary % 10
        decimal += last * base
        binary //= 10
        base *= 2
    
    return decimal

#print(conBtodec(1010))
 

# Decimal to binary conversion
def conDtobin(decimal):
    binary_str = ""

    if decimal == 0:
        return "0000"

    while decimal > 0:
        r = decimal % 2
        binary_str = str(r) + binary_str
        decimal //= 2

    # Calculate the number of leading zeros needed for padding
    pad_length = (4 - len(binary_str) % 4) % 4

    # Pad with leading zeros if necessary
    if pad_length > 0:
        binary_str = '0' * pad_length + binary_str

    return binary_str

def permute(key, arr, num):
    permutation = ""

    i = 1
    for i in range(0, num):
        adjust = arr[i] - 1
        permutation += key[adjust]
    
    return permutation

def shift_left(binary_str, num):
    return binary_str[num:] + binary_str[:num]


def xor(binary1, binary2):
    result = ""
    for i in range(len(binary1)):
        if binary1[i] == binary2[i]:
            result = result + "0"
        else:
            result = result + "1"
    return result
 
########################################## Key and Box Storage ##########################################

parity_key = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Permutation tables
per = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]

perm1 = [58, 50, 42, 34, 26, 18, 10, 2,
         60, 52, 44, 36, 28, 20, 12, 4,
         62, 54, 46, 38, 30, 22, 14, 6,
         64, 56, 48, 40, 32, 24, 16, 8,
         57, 49, 41, 33, 25, 17, 9, 1,
         59, 51, 43, 35, 27, 19, 11, 3,
         61, 53, 45, 37, 29, 21, 13, 5,
         63, 55, 47, 39, 31, 23, 15, 7]

perm2 = [40, 8, 48, 16, 56, 24, 64, 32,
         39, 7, 47, 15, 55, 23, 63, 31,
         38, 6, 46, 14, 54, 22, 62, 30,
         37, 5, 45, 13, 53, 21, 61, 29,
         36, 4, 44, 12, 52, 20, 60, 28,
         35, 3, 43, 11, 51, 19, 59, 27,
         34, 2, 42, 10, 50, 18, 58, 26,
         33, 1, 41, 9, 49, 17, 57, 25]
 
# D-box
dbox = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]
 
 
# S-boxes
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
 
########################################## MAIN FUNCTIONS ##########################################

def encrypt(message, round_key_binary, rk):
    message = converthex(message)
 
    # Permute 1
    message = permute(message, perm1, 64)
 
    # Splitting the messagw
    left = message[0:32]
    right = message[32:64]

    for i in range(0, 16):
        right_expanded = permute(right, dbox, 48)
        x_result = xor(right_expanded, round_key_binary[i])
 
        # S-boxex: substituting the value from s-box table by calculating row and column
        s_result = ""
        for j in range(0, 8):
            row = conBtodec(int(x_result[j * 6] + x_result[j * 6 + 5]))
            col = conBtodec(
                int(x_result[j * 6 + 1] + x_result[j * 6 + 2] + x_result[j * 6 + 3] + x_result[j * 6 + 4]))
            val = sbox[j][row][col]
            s_result = s_result + conDtobin(val)
 
        # Straight D-box: After substituting rearranging the bits
        s_result = permute(s_result, per, 32)
 
        # XOR left and s_result
        result = xor(left, s_result)
        left = result
 
        # Swapper
        if(i != 15):
            left, right = right, left
 
    # Glue them back together
    combine = left + right
 
    # Permute 2
    cipher_text = permute(combine, perm2, 64)
    return cipher_text
 
 
# Key generation
key = converthex(key)
 
# Getting 56 bit key from 64 bit using the parity bits
key = permute(key, parity_key, 56)
 
# Number of bit shifts per round
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]
 
# Compression key from 56 to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]
 
# Splitting of the key
left = key[0:28]
right = key[28:56]
 
round_key_binary = []
rk = []

# Round key generation with perute function and key_comp
for i in range(0, 16):
    
    # Shifting 
    left = shift_left(left, shift_table[i])
    right = shift_left(right, shift_table[i])
 
    # Combination of left and right string
    combine_str = left + right
 
    # Compression of key from 56 to 48 bits
    round_key = permute(combine_str, key_comp, 48)
 
    round_key_binary.append(round_key)
    rk.append(convertbinary(round_key))
 
# Encrypt
cipher_text = convertbinary(encrypt(message, round_key_binary, rk))
print("Cipher: ", cipher_text)

# Revert and send back through the network
reversed_round_key_binary = round_key_binary[::-1]
reversed_round_key = rk[::-1]

# Send back through
text = convertbinary(encrypt(cipher_text, reversed_round_key_binary, reversed_round_key))
print("Message:", text)
