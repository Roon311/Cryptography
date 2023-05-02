from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import time
import numpy as np
import os
import re

import ut
def encryptor(key, plaintext, length=128):
    assert length % 8 == 0
    num_octet = length // 8
    BS = num_octet
    ciphertext = b''
    plaintext = plaintext.encode(encoding='utf8')  # Convert data to bytes
    iv = ut.initialization(num_octet)
    fr = iv
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    prefix = os.urandom(num_octet + 2)
    fre = cipher.encrypt(fr)
    C=bytes([f ^ b for f, b in zip(fre,prefix[0:BS])])
    ciphertext +=C
    fr=C#Load FR with C[1] through C[BS]
    fre = cipher.encrypt(fr)


    C_bs_plus_1_2 = bytes([f ^ prefix[BS+i] for i, f in enumerate(fre[:2])])
    ciphertext+=C_bs_plus_1_2
   # print('-------------------------')
   # print(prefix)
   # print('-------------------------')

    # resynchronization
    fr = fr[2:] + C_bs_plus_1_2#FR is loaded with C[3] through C[BS+2]
    while plaintext:
        if(len(plaintext)<BS):
            plaintext=pad(plaintext,BS)
        data=plaintext[:BS]
        fre = cipher.encrypt(fr)
        ciphertext_block = bytes([f ^ b for f, b in zip(fre, data)])
        ciphertext+=ciphertext_block
        fr=ciphertext_block
        plaintext = plaintext[BS:]
    return ciphertext

def decryptor(key, ciphertext,length=128):
    assert length % 8 == 0
    num_octet = length // 8
    BS = num_octet
    iv = ut.initialization(num_octet)
    fr = iv
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    fre = cipher.encrypt(fr)
    prefix = bytes([f ^ b for f, b in zip(fre, ciphertext[0:16])])     
    fr=ciphertext[0:16]
    fre = cipher.encrypt(fr)
    prefix2 = bytes([f1 ^ c1 for f1, c1 in zip(fre[:2],ciphertext[16:18])])
    prefix+=prefix2         # I am having an issue with the prefix
    
   # print('-------------------------')
   # print(prefix)
   # print('-------------------------')

    fr=ciphertext[2:18]
    fre = cipher.encrypt(fr)
    c=ciphertext[18:34]
    plaintext= bytes([f ^ b for f, b in zip(fre, c)])
    ciphertext=ciphertext[34:]
    fr=c
    while ciphertext:
      data=ciphertext[:BS]
      fre = cipher.encrypt(fr)
      plaintext_block = bytes([f ^ b for f, b in zip(fre, data)])
      plaintext+=plaintext_block
      fr=data
      ciphertext=ciphertext[BS:]
    if ut.is_pkcs7_padded(plaintext)==True:
        plaintext=unpad(plaintext,BS)
    return plaintext.decode(encoding='utf8')

def tester(path,key= get_random_bytes(16)):
    Text=ut.getText(path)
    start = time.time()
    ciphertext = encryptor(key,Text)
    end =time.time()
    encryption_time=end-start
    start = time.time()
    plaintext=decryptor(key, ciphertext)
    end =time.time()
    decryption_time=end-start
    return Text,ciphertext,encryption_time,plaintext,decryption_time

