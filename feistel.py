from helpers import *

"""
This is a simple block cipher based on a Feistel network. The size of the blocks
is 64 bits, and the round function F(x) is given by 

                F(x,k) = x^2k + xk^2
                
x is the right half of the input, and k is the round key.

Multiplication is performed in the finite field F_2^32 given by the irreducible
polynomial p(x) = x^32 + x^15 + x^9 + x^7 + x^4 + x^3 + 1

The cipher consists of 8 rounds.
The key K is 32 bits long, and the round keys are derived from it by 4-bit cyclic
shifts, i.e. the first round key is k1 = K; the second round key k2 is obtained by
cyclically shifting K 4 bits to the right; and so forth
"""


# irreducible polynomial
irr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1]
keys = []


"""
8 keys is created by cyclically shifting 
the key 4 bits to the right
Each of these keys are then used in each of the
rounds in the round function (round_i(k_i))
"""
def key_shift(key):
    result = []
    intermediate = key.copy()
    for i in range(8):
        if i == 0:  # K1 = key
            result.append(key)
            continue
        for j in range(4):
            new_first = intermediate.pop()
            intermediate.insert(0, new_first)
        result.append(intermediate.copy())
    return result


"""
:param input 64bit long string
:param round the current round of the round function
:param mode either encryption or decryption
"""
def feistel(input, round, mode):
    output = []
    """INPUT"""
    if (mode == "encrypt"):
        if isinstance(input, str):
            left_half = split_word(split_input(input)[0])
            left_half_output = split_word(split_input(input)[1])
        else:
            left_half = input[:32]
            left_half_output = input[32:]
    elif (mode == "decrypt"):
        keys.reverse()  ## reverse the order of the keys
        if isinstance(input, str):
            left_half = split_word(split_input(input)[1])
            left_half_output = split_word(split_input(input)[0])
        else:
            left_half = input[32:]
            left_half_output = input[:32]
    else:
        raise AssertionError(f"expected 'encrypt' or 'decrypt', was '{mode}'")

    """function"""
    x_2 = multiplication(left_half_output, left_half_output, irr)
    x_2_times_k = multiplication(x_2, keys[round], irr)

    k_2 = multiplication(keys[round], keys[round], irr)
    x_times_k_2 = multiplication(left_half_output, k_2, irr)

    function_output = xor(x_2_times_k, x_times_k_2)
    final_rightHalf = xor(left_half, function_output)

    if (mode == "encrypt"):
        # first add left half
        output += left_half_output
        # then right half
        output += final_rightHalf
    else:
        # first add right half
        output += final_rightHalf
        # then left half
        output += left_half_output
        keys.reverse()  # reverse again, or else next round the list will be reversed back to original

    return output

"""
:param str is split into strings of 64bit binary blocks
:param key the key used to encrypt
"""
def encrypt(str, key):
    global keys
    """key schedule"""
    keys = key_shift(split_word(key))
    encrypted = []
    encrypted_string = ""
    for block in string_to_binary(str):
        for i in range(8):
            next = feistel(block, i, "encrypt")
            block = next
        encrypted.append(list_to_string(block))
        encrypted_string += list_to_string(block)
    return encrypted_string


"""
:param str is split into strings of 64bit blocks
:param key the key used to encrypt
"""
def decrypt(str, key):
    global keys
    """key schedule"""
    keys = key_shift(split_word(key))
    decrypted_ = ""
    encrypted_blocks = [str[index: index + 64] for index in range(0, len(str), 64)]
    for block in encrypted_blocks:
        for i in range(8):
            next = feistel(block, i, "decrypt")
            block = next
        decrypted_ += list_to_string(block)
    return binary_to_ascii(decrypted_)
