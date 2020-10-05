import binascii
import numpy as np

def split(word):
    return [char for char in word]

def permute(input, table):
    output = []

    for x in range(len(table)):
        output.append('0')

    for i in range(len(table)):
        output[i] = input[table[i]-1]

    return output

def shift(input_arr, d):
    output = np.roll(input_arr, -d)
    return output

def process_key(new_k):
    pc_1 = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    k_pc_1 = [0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0]

    k_arr = ''.join(new_k)
    k_arr = list(k_arr)

    k_pc_1 = permute(k_arr, pc_1)

    c_0 = k_pc_1[:len(k_pc_1)//2]
    d_0 = k_pc_1[len(k_pc_1)//2:]

    c = np.zeros((17, 28))
    d = np.zeros((17,28))

    shift_num = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    c[0] = c_0
    d[0] = d_0

    i = 0

    while i < len(shift_num):
        c[i+1] = shift(c[i], shift_num[i])
        d[i+1] = shift(d[i], shift_num[i])

        i += 1

    pc_2 = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]


    k_pre = np.concatenate((c, d), axis=1)

    k_fin = np.zeros((17,48))

    i = 1
    while i < 17:
        k_fin[i] = permute(k_pre[i], pc_2)
        k_fin[i] = k_fin[i].astype(np.int)

        i += 1


    return k_fin

def f(r, k):
    e = [32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1]

    e_r = permute(r, e)
    e_r = [int(i) for i in e_r]

    k = [int(i) for i in k]

    xored = []

    for i in range(len(k)):
        xored.append(k[i] ^ e_r[i])

    temp = '{}' * 6
    xored = [temp.format(*ele) for ele in zip(*[iter(xored)] * 6)]

    s1 = np.array([[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])
    s2 = np.array([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])
    s3 = np.array([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])
    s4 = np.array([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])
    s5 = np.array([[2, 12, 4, 1, 7, 10, 11, 6, 7, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])
    s6 = np.array([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])
    s7 = np.array([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])
    s8 = np.array([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])

    s = []

    for i in range(len(xored)):
        temp1 = xored[i][0] + xored[i][-1]
        temp2 = xored[i][1:-1]

        temp1 = int(temp1, 2)
        temp2 = int(temp2, 2)

        if i == 0:
            s.append(bin(s1.item(temp1, temp2)))
        elif i == 1:
            s.append(bin(s2.item(temp1, temp2)))
        elif i == 2:
            s.append(bin(s3.item(temp1, temp2)))
        elif i == 3:
            s.append(bin(s4.item(temp1, temp2)))
        elif i == 4:
            s.append(bin(s5.item(temp1, temp2)))
        elif i == 5:
            s.append(bin(s6.item(temp1, temp2)))
        elif i == 6:
            s.append(bin(s7.item(temp1, temp2)))
        elif i == 7:
            s.append(bin(s8.item(temp1, temp2)))
                
    for x in range(len(s)):
        s[x] = s[x][2:]
    
        if len(s[x]) != 4:
            zta = 4 - len(s[x])
            s[x] = s[x].rjust(zta + len(s[x]), '0')

    s = ''.join(s)
    s = list(s)
       
    p = [16, 7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2, 8, 24, 14,
            32, 27, 3, 9,
            19, 13, 30, 6,
            22, 11, 4, 25]

    s_fin = permute(s, p)

    s_fin = [int(i) for i in s_fin]

    return s_fin

def des_encrypt(m, k):

    # Process m and split it into left and right halves

    m = split(m)
    for x in range(len(m)):
        m[x] = bin(int(m[x], 16))

        m[x] = m[x][2:]

        if len(m[x]) != 4:
            zta = 4 - len(m[x])
            m[x] = m[x].rjust(zta + len(m[x]), '0')

    m = ''.join(m)
    m = list(m)

    l = m[:len(m)//2]
    r = m[len(m)//2:]

    # Process the 64-bit key

    k = split(k)
    for x in range(len(k)):
        k[x] = bin(int(k[x], 16))

        k[x] = k[x][2:]

        if len(k[x]) != 4:
            zta = 4 - len(k[x])
            k[x] = k[x].rjust(zta + len(k[x]), '0')

    new_k = []
    x = 0
    while x < len(k):
        k_str = k[x] + k[x+1]
        new_k.append(k_str)
        x = x + 2

    proc_k = process_key(new_k)

    ip = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

    m_ip = permute(m, ip)

    l_0 = m_ip[:len(m_ip)//2]
    r_0 = m_ip[len(m_ip)//2:]

    l_0 = [int(numeric_string) for numeric_string in l_0]
    r_0 = [int(numeric_string) for numeric_string in r_0]

    l = np.zeros((17, 32))
    r = np.zeros((17, 32))

    l[0] = l_0
    r[0] = r_0

    l[0] = [int(i) for i in l[0]]
    r[0] = [int(i) for i in r[0]]

    #f_var = f(r[i - 1], proc_k[i])

    n = 1
    while n < 17:
        f_var = f(r[n-1], proc_k[n])

        l[n] = r[n-1]
        r[n] = [(int(l.item((n-1), x)) ^ f_var[x]) for x in range(len(r[n-1]))]

        n += 1
   
    m_en = np.append(r[16], l[16])

    ip_inv = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9,  49, 17, 57, 25]

    encrypted = permute(m_en, ip_inv)
    encrypted = [int(i) for i in encrypted]

    temp = '{}' * 8                                                                                               
    encrypted = [temp.format(*ele) for ele in zip(*[iter(encrypted)] * 8)]

    for i in range(len(encrypted)):
        encrypted[i] = hex(int(encrypted[i], 2))
        #encrypted[i] = encrypted[i][2:]

    encrypted = ' '.join(encrypted)

    return encrypted

m = "0123456789ABCDEF"
k = "133457799BBCDFF1"

print(des_encrypt(m, k))
