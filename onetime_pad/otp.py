import argparse
import os
import sys

def encrypt(message, key):
    if(len(message) <= len(key)):

        encrypted = []

        for i in range(len(message)):
            xor_val = ord(message[i]) ^ ord(key[i])
            encrypted.append(xor_val)

        for i in range(len(encrypted)):
            encrypted[i] = chr(encrypted[i])
    
        return ''.join(encrypted)

    else:
        return "Your key must be at least as long as the message!!"

def decrypt(encrypted, key):
    decrypted = []

    for i in range(len(encrypted)):
        xor_val = ord(encrypted[i]) ^ ord(key[i])
        decrypted.append(xor_val)

    for i in range(len(decrypted)):
        decrypted[i] = chr(decrypted[i])

    return ''.join(decrypted)

parser = argparse.ArgumentParser(description="Encrypt or decrypt files via one-time pad")
parser.add_argument('-e', '--encrypt', action='store_true', help="Encrypt the target file with the key file")
parser.add_argument('-d', '--decrypt', action='store_true', help="Decrypt the target file with the key file")
parser.add_argument('Target', metavar="target-path", type=str, help="Path to the target file")
parser.add_argument('Key', metavar="key-path", type=str, help="Path to the key file")
parser.add_argument('Output', metavar='output-path', type=str, help='Path to the output file')

args = parser.parse_args()

enc = args.encrypt
dec = args.decrypt
message_path = args.Target
key_path = args.Key
out_path = args.Output

m_file = open(message_path, "r")
m = m_file.read()

k_file = open(key_path, "r")
k = k_file.read()

o_file = open(out_path, "w")

if enc:
    o_file.write(encrypt(m, k))
    sys.exit()
elif dec:
    o_file.write(decrypt(m, k))
    sys.exit()
else:
    print('ERR: You must specify an operation')
    sys.exit()


