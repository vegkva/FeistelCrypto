"""Splits word into list as integers"""


def split_word(word):
    return [int(char) for char in word.replace(" ", "")]


def binary_to_ascii(str):
    binary_int = int(str, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode(errors='ignore')
    return ascii_text



"""
Function to convert user input from string
to a list containing 64bit binary representation
of the original string

If the string is not long enough to fill 64bit,
the string will be prefixed with zeroes until
the string is 64bit

Example: 'a' -> 01100001 is only 8bits. Will therefore be prefixed with 64-8 zeroes:
-> 0000000000000000000000000000000000000000000000000000000001100001
"""
def string_to_binary(str):
    list = []
    for char in str:
        hex_val = int(hex(ord(char)), 16)
        if hex_val == 8217:
            hex_val = 39
        list.append(format(hex_val, '08b'))
    complete_plaintext = []
    list1 = list
    intermediate = []
    while len(list1) > 0:
        intermediate = list[0:8]
        while len(list_to_string(intermediate)) != 64:
            intermediate.insert(0, "00000000")
        del list1[0:8]
        complete_plaintext.append(list_to_string(intermediate))
        intermediate.clear()
    return complete_plaintext


def split_input(input):
    result = [input[:-32], input[32:]]
    return result


def list_to_string(list):
    result = ""
    for bit in list:
        result += str(bit)
    return result


# __source__ = INF143a lecture
def xor(v1, v2):
    result = []
    for i in range(len(v1)):
        result.append((v1[i] + v2[i]) % 2)
    return result


# __source__ = INF143a lecture
"""Function to multiply to vectors. Modulation"""
def multiplication(A, B, irr):
    result = []  # intermediate state
    for i in range(len(A)):
        result.append(0)

    for i in range(len(A)):
        if B[i] == 1:
            shift = A
            for s in range(i):
                do_we_have_overflow = (shift[-1] == 1)
                shift = [0] + shift[:-1]
                if do_we_have_overflow:
                    shift = xor(shift, irr)
            result = xor(result, shift)
    return result
