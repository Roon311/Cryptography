from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import time
import numpy as np
import ut
import os
import re


def encryptor(key, plaintext, length=128):
    # 1 octet=8bits
    assert length % 8 == 0
    num_octet = length // 8
    BS = num_octet
    hamada=[]
    # Prepare and text
    plaintext = plaintext.encode(encoding='utf8')  # Convert data to bytes
    print(plaintext)
    #ut.unicodetoascii( str(data) )
    # Prepare the initialization vector
    iv = ut.initialization(num_octet)
    # Initialize the feedback register (FR) with the IV.
    fr = iv
    # Initialize the AES cipher with the key and IV
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    print(len(fr))
    ciphertext = b''
    prefix = os.urandom(num_octet + 2)
    print(f'prefix:{prefix[0:16]}')
    print(f'prefix:{prefix[16:]}')
    fre = cipher.encrypt(fr)
    C=bytes([f ^ b for f, b in zip(fre,prefix[0:BS])])#XOR FRE with the first BS octets of the prefixed plaintext to produce C[1] through C[BS], the first BS octets of ciphertext.
    ciphertext +=C #first BS
    fr=C#Load FR with C[1] through C[BS].
    fre = cipher.encrypt(fr)
    C_bs_plus_1_2 = bytes([f ^ prefix[i] for i, f in enumerate(fre[:2])])#The left two octets of FRE get xored with the next two octets of data that were prefixed to the plaintext.  This produces C[BS+1]and C[BS+2], the next two octets of ciphertext.
    ciphertext+=C_bs_plus_1_2#next 2 octets of the ciphertext
    
    # resynchronization
    print("-----Index3--------")
    print('fre=',fre[:2])
    print('cipher 17, 18',C_bs_plus_1_2)
    print(C_bs_plus_1_2,fre[:2])
    print(f'prefix2:{prefix[16:]}')
    prefix2 = ([f1 ^ c1 for f1, c1 in zip(C_bs_plus_1_2,fre[:2] )])
    print(f'prefix2:{prefix2}')
    prefix2 = bytes([f1 ^ c1 for f1, c1 in zip(fre[:2],C_bs_plus_1_2 )])
    print(f'prefix2:{prefix2}')
    prefix2 = bytes([f ^ C_bs_plus_1_2[i] for i, f in enumerate(fre[:2])])#The left two octets of FRE get xored with the next two octets of data that were prefixed to the plaintext.  This produces C[BS+1]and C[BS+2], the next two octets of ciphertext.
    print(f'prefix2:{prefix2}')
    print(C_bs_plus_1_2)

    print("-----Index3-18--------")
    print(fr[2:] + C_bs_plus_1_2)
    fr = fr[2:] + C_bs_plus_1_2#FR is loaded with C[3] through C[BS+2]
    Nour=plaintext[:BS]
    while plaintext:
    # Encrypt the FR using the AES encryption algorithm to obtain the encrypted feedback register (FRE).
        if(len(plaintext)<BS):
            print(len(plaintext))
            #pad_len = num_octet - (len(plaintext) % num_octet)
            #plaintext = plaintext + bytes([pad_len] * pad_len)
            plaintext=pad(plaintext,BS)
            print(len(plaintext))
        data=plaintext[:BS]
        # Prefix the plaintext
        #print("fr",fr)
        fre = cipher.encrypt(fr)#FR is encrypted to produce FRE.
        hamada.append(fre)
        ciphertext_block = bytes([f ^ b for f, b in zip(fre, data)])
        #print(data)
        #print(fre)
        #print(ciphertext_block)
        ciphertext+=ciphertext_block
        fr=ciphertext_block
        plaintext = plaintext[BS:]
    return ciphertext,Nour,hamada

def decryptor(key, ciphertext,Nour,hamada, length=128):
    
    assert length % 8 == 0
    num_octet = length // 8
    BS = num_octet
    iv = ut.initialization(num_octet)
    fr = iv
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    fre = cipher.encrypt(fr)
    #xor the fre with first 16bytes of cipher text to get first 16 bytes of prefix
    prefix = bytes([f ^ b for f, b in zip(fre, ciphertext[0:16])])
    print(prefix)
    fr=ciphertext[0:16]
    print("-----Index3-------")
    print(fr)
    print("-----Index3-18--------")
    fre = cipher.encrypt(fr)
    print('fre[0:2]',fre[0:2])   
    print('Cipher 17,18:',ciphertext[16:18]) 
    prefix2 = bytes([f1 ^ c1 for f1, c1 in zip(fre[:2],ciphertext[16:18] )])
    print(f'prefix2:{prefix2}')
    print(prefix2)
    fr=ciphertext[2:18]
    print("-----Index3-18--------")
    print(fr)
    fre = cipher.encrypt(fr)
    c=ciphertext[18:34]
    #fre=hamada[0]
    plaintext= bytes([f ^ b for f, b in zip(fre, c)])
    print("fre",fre)
    print(plaintext)
    ci=bytes([f ^ b for f, b in zip(fre, Nour)])
    print(ci)






    #34 bits by 34 bits
    #first 18 bytes of cipher text prefix
    #followed by BS of data

    plaintext = b''

    i = BS
    while ciphertext:
        data=plaintext[:(BS+BS+2)]
        fre = cipher.encrypt(fr)
        C = bytes([f ^ b for f, b in zip(fre, prefix[0:BS])])
        fr = C

        C_bs_plus_1_2 = bytes([f ^ prefix[i] for i, f in enumerate(fre[:2])])
        fr = fr[2:] + C_bs_plus_1_2
        fre = cipher.encrypt(fr)

        ciphertext_block = ciphertext[i:i+BS]
        plaintext_block = bytes([f ^ b for f, b in zip(fre, ciphertext_block)])
        plaintext += plaintext_block

        i += BS

    #plaintext = unpad(plaintext, BS)

    return plaintext#.decode('utf-8')






key = get_random_bytes(16)
start = time.time()
ciphertext,Nour,hamada = encryptor(key, 'Hello there my friend\n I know life has been tough.')
end =time.time()
decryptor(key, ciphertext,Nour,hamada)
#restored=decryptor(key, ciphertext)
#plaintext = ut.unicodetoascii( str(restored) ).replace("\\n","\n")[2:-1]
#decrypted_plaintext = ut.unicodetoascii( str(restored) ).replace("\\n","\n")[2:-1]
print(f'Cipher text is: {ciphertext}')
#print(f'decry text is: {restored}')
print(f'Time taken is{end-start}')



#Old encryptor
'''
def encryptor(key, plaintext, length=128):
    # 1 octet=8bits
    assert length % 8 == 0
    num_octet = length // 8
    BS = num_octet
    # Prepare and text


    plaintext = plaintext.encode(encoding='utf8')  # Convert data to bytes
    print(plaintext)
    #ut.unicodetoascii( str(data) )
    # Prepare the initialization vector
    iv = ut.initialization(num_octet)
    # Initialize the feedback register (FR) with the IV.
    fr = iv
    # Initialize the AES cipher with the key and IV
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    print(len(fr))
    ciphertext = b''
    
    while plaintext:
    # Encrypt the FR using the AES encryption algorithm to obtain the encrypted feedback register (FRE).
        if(len(plaintext)<BS):
            print(len(plaintext))
            #pad_len = num_octet - (len(plaintext) % num_octet)
            #plaintext = plaintext + bytes([pad_len] * pad_len)
            plaintext=pad(plaintext,BS)
            print(len(plaintext))
        data=plaintext[:BS]
        fre = cipher.encrypt(fr)
        # Prefix the plaintext
        prefix = os.urandom(num_octet + 2)
        data_pre = prefix + data
        print(len(data_pre))
        C=bytes([f ^ b for f, b in zip(fre,prefix[0:BS])])#XOR FRE with the first BS octets of the prefixed plaintext to produce C[1] through C[BS], the first BS octets of ciphertext.
        ciphertext +=C #first BS
        fr=C#Load FR with C[1] through C[BS].
        fre = cipher.encrypt(fr)
        C_bs_plus_1_2 = bytes([f ^ prefix[i] for i, f in enumerate(fre[:2])])#The left two octets of FRE get xored with the next two octets of data that were prefixed to the plaintext.  This produces C[BS+1]and C[BS+2], the next two octets of ciphertext.
        ciphertext+=C_bs_plus_1_2#next 2 octets of the ciphertext
        # resynchronization
        fr = fr[2:] + C_bs_plus_1_2#FR is loaded with C[3] through C[BS+2]
        fre = cipher.encrypt(fr)#FR is encrypted to produce FRE.
        ciphertext_block = bytes([f ^ b for f, b in zip(fre, data)])
        ciphertext+=ciphertext_block
        fr=ciphertext_block
        plaintext = plaintext[BS:]
    return ciphertext

'''