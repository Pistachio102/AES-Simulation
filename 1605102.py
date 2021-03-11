from BitVector import *

import bitvector_demo
import codecs
from collections import deque

count = 0
bv1 = 00
def Convert_to_list(string):
    list1=[]
    list1[:0]=string
    return list1

def Convert_to_hex(list):
    hex_list = []
    for i in list:
        hex_list.append(hex(ord(i)))
    return hex_list
def XOR(l1, l2):
    new_list = []
    lenth = len(l1)
    c = 0;
    while c < lenth:
        element = hex(int(l1[c], 16) ^ int(l2[c], 16))[2:4]
        new_list.append(element)
        #print(element)
        c += 1
    return new_list

def g(list):
    global count
    global bv1
    count += 1
    g_list = []
    queue = deque(list)
    #Circular byte left shift
    queue.rotate(-1)


    #Byte substitution
    for i in queue:
        hex_val = str(i)
        #print(hex_val)
        b = BitVector(hexstring=hex_val)
        int_val = b.intValue()
        s = bitvector_demo.Sbox[int_val]
        s = BitVector(intVal=s, size=8)
        g_list.append(s.get_bitvector_in_hex())
        #print(s.get_bitvector_in_hex())
    #print(g_list)
    #Adding round constant
    if count == 1:
        bv3 = BitVector(hexstring="01")

        bv1 = bv3
    else:
        bv2 = BitVector(hexstring="02")
        bv3 = bv1.gf_multiply_modular(bv2, bitvector_demo.AES_modulus, 8)
        bv1 = bv3

    sbyte = []
    sbyte.append(g_list[0])
    rc = []
    #print(hex(bv3.intValue()))
    rc.append(hex(bv3.intValue()))
    added = XOR(sbyte, rc)
    g_list[0] = added[0]
    #print(g_list[0])
    return g_list


def Append_to_the_list(a1, a2, a3, a4):
    list = []
    list.append(a1)
    list.append(a2)
    list.append(a3)
    list.append(a4)
    return list


def Generate_round_keys(key_list):
    level = 0
    all_level_round_keys = []
    w0 = key_list[0:4]
    w1 = key_list[4:8]
    w2 = key_list[8:12]
    w3 = key_list[12:16]
    #print(w3)
    zero_level_key = Append_to_the_list(w0, w1, w2, w3)
    all_level_round_keys.append(zero_level_key)


    while level < 10:
        w4 = XOR(w0, g(w3))
        w5 = XOR(w1, w4)
        w6 = XOR(w2, w5)
        w7 = XOR(w3, w6)
        new_level_key = Append_to_the_list(w4, w5, w6, w7)
        all_level_round_keys.append(new_level_key)
        w0 = w4
        w1 = w5
        w2 = w6
        w3 = w7
        level += 1
    for i in all_level_round_keys:
        print(i)
    return all_level_round_keys



def Schedule_key():

    key = input('Enter a key: ')
    length_of_key = len(key)

    if length_of_key < 16:
        count = 16 - length_of_key
        i = 1
        while i <= count:
            key += '0'
            i = i + 1
    elif length_of_key > 16:
        key = key[0: 16: ]
        #print(key)

    hex_list = Convert_to_hex(key)
    i = 0
    while i < len(hex_list):
        hex_list[i] = str(hex_list[i])[2: 4: ]
        i += 1
    #print(hex_list)
    Generate_round_keys(hex_list)


if __name__ == '__main__':

    Schedule_key()