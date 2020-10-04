import binascii

def split(word): 
    return [char for char in word]  

def des_encrypt(m, k):
    # Process m and split it into left and right halves
    m = split(m)
    for x in range(len(m)):
        m[x] = bin(int(m[x], 16)) 

        m[x] = m[x][2:]

        if len(m[x]) != 4:
            zta = 4 - len(m[x])
            m[x] = m[x].rjust(zta + len(m[x]), '0')

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

    return k


m = "0123456789ABCDEF"
k = "133457799BBCDFF1"

print(des_encrypt(m, k))
