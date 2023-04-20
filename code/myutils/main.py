from Crypto.Random import get_random_bytes
import PGP as pgp 
import ut
import time

#Testing on 1kb
key = get_random_bytes(16)
originaltext,ciphertext,encryption_time,plaintext,decryption_time=pgp.tester('TestFiles/1KB_file.txt',key)
ut.drawer(originaltext,ciphertext,encryption_time,plaintext,decryption_time)
#Testing on 5kb
key = get_random_bytes(16)
originaltext,ciphertext,encryption_time,plaintext,decryption_time=pgp.tester('TestFiles/5KB_file.txt',key)
ut.drawer(originaltext,ciphertext,encryption_time,plaintext,decryption_time)
#Testing on 10KB
key = get_random_bytes(16)
originaltext,ciphertext,encryption_time,plaintext,decryption_time=pgp.tester('TestFiles/10KB_file.txt',key)
ut.drawer(originaltext,ciphertext,encryption_time,plaintext,decryption_time)
#Testing on 100KB
key = get_random_bytes(16)
originaltext,ciphertext,encryption_time,plaintext,decryption_time=pgp.tester('TestFiles/100KB_file.txt',key)
ut.drawer(originaltext,ciphertext,encryption_time,plaintext,decryption_time)
