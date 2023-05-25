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
    num_octet = length // 8 #Divide by 8 to get number of bytes
    BS = num_octet #Block size =number of bytes
    ciphertext = b'' #Empty byte to hold the obtained ciphertext
    plaintext = plaintext.encode(encoding='utf8')  # Convert data to bytes
    iv = ut.initialization(num_octet) #Form the initialization vector
    fr = iv #fr is initially set similar to the initialization vector
    cipher = AES.new(key, AES.MODE_CFB, iv=iv) #Form the AES cipher object with CFB mode
    prefix = os.urandom(num_octet) #Form BS+2 random prefix 
    resyncho=prefix[14:]
    prefix+=resyncho
    fre = cipher.encrypt(fr) #Encrypt the fr
    print(fre[14:16],len(fre[14:16]))
    
    C=bytes([f ^ b for f, b in zip(fre,prefix[0:BS])]) #Xor the perfix with the fre to get the first 16 bytes of the ciphered text
    ciphertext +=C #concate the the produced ciphertext bytes to the ciphertext byte array
    fr=C#Load FR with C[1] through C[BS]
    fre = cipher.encrypt(fr)#Encrypt the fr


    C_bs_plus_1_2 = bytes([f ^ prefix[BS+i] for i, f in enumerate(fre[:2])])#Get ciphertext byte 17, and 18
    ciphertext+=C_bs_plus_1_2


    # resynchronization
    fr = fr[2:] + C_bs_plus_1_2#FR is loaded with C[3] through C[BS+2]
    #Start encrypting the actual plaintext
    while plaintext:
        if(len(plaintext)<BS):
            plaintext=pad(plaintext,BS)#if the last section of the plaintext is less than BS PCKS7 pad it
        data=plaintext[:BS]#dividing the plaintext into blocks of BS
        fre = cipher.encrypt(fr) #Encrypt the fr
        ciphertext_block = bytes([f ^ b for f, b in zip(fre, data)]) #Byte 19-34 of the ciphertext them 35-50 and so on
        ciphertext+=ciphertext_block #add to the byte array
        fr=ciphertext_block
        plaintext = plaintext[BS:]
    return ciphertext

def decryptor(key, ciphertext,length=128,oracle=False):
    assert length % 8 == 0
    num_octet = length // 8
    BS = num_octet
    iv = ut.initialization(num_octet)
    fr = iv#fr is initially set similar to the initialization vector
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)#Form the AES cipher object with CFB mode
    fre = cipher.encrypt(fr)#Encrypt the fr
    prefix = bytes([f ^ b for f, b in zip(fre, ciphertext[0:16])])  #Restoring the prefix 16 bytes   
    fr=ciphertext[0:16]
    fre = cipher.encrypt(fr)
    prefix2 = bytes([f1 ^ c1 for f1, c1 in zip(fre[:2],ciphertext[16:18])]) #Restoring BS+1,BS+2 of the prefix
    prefix+=prefix2 #Restoring the full prefix
    if oracle==True:
        fr = iv
        cipher = AES.new(key, AES.MODE_ECB)#Form the AES cipher object with CFB mode
        fre = cipher.encrypt(fr)#Encrypt the fr
        prefix = bytes([f ^ b for f, b in zip(fre, ciphertext[0:16])])  #Restoring the prefix 16 bytes   
        fr=ciphertext[0:16]
        fre = cipher.encrypt(fr)
        prefix2 = bytes([f1 ^ c1 for f1, c1 in zip(fre[:2],ciphertext[16:18])]) #Restoring BS+1,BS+2 of the prefix
        prefix+=prefix2 #Restoring the full prefix
        return prefix
    fr=ciphertext[2:18]
    fre = cipher.encrypt(fr)#Encrypt the fr
    c=ciphertext[18:34]
    plaintext= bytes([f ^ b for f, b in zip(fre, c)])
    ciphertext=ciphertext[34:]
    fr=c
    while ciphertext:
      data=ciphertext[:BS]
      fre = cipher.encrypt(fr)#Encrypt the fr
      plaintext_block = bytes([f ^ b for f, b in zip(fre, data)])
      plaintext+=plaintext_block
      fr=data
      ciphertext=ciphertext[BS:]
    if ut.is_pkcs7_padded(plaintext)==True: #if there is padding
        plaintext=unpad(plaintext,BS)#remove the padding
    return plaintext.decode(encoding='utf8')#convert bytes to string

def tester(path,key= get_random_bytes(16)):
    Text=ut.getText(path) #Read the file
    start = time.time() #get current time
    ciphertext = encryptor(key,Text) # Encrypt
    end =time.time() #get current time
    encryption_time=end-start #Encryption time
    start = time.time()#get current time
    plaintext=decryptor(key, ciphertext) #Decrypt
    end =time.time()#get current time
    decryption_time=end-start#Decryption time
    return Text,ciphertext,encryption_time,plaintext,decryption_time

