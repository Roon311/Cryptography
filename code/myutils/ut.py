def initialization(num_octet:int):
    iv = b'\x00' * (num_octet)
    #print(len(iv))
    #print('---------------------------initialization vector-----------------\n')
    #print(f'{iv} \n')
    #print('-----------------------------------------------------------------\n')
    return iv

def is_pkcs7_padded(data):
    last_byte = data[-1]
    if last_byte > 16:
        return False
    for i in range(len(data) - last_byte, len(data)):
        if data[i] != last_byte:
            return False
    return True

def getText(path):
    with open('TestFiles/1KB_file.txt','r', encoding='utf8') as file:
        Text = file.read()
    return Text

def WriteResults(filename):
    filenamee = filename+".txt"
    #file.write()
    #file.close()
    try:
        file = open(filename, "r+")  # open file for reading and writing
    except FileNotFoundError:
        file = open(filename, "w+")  # create file if it doesn't exist
    return file

def drawer(originaltext,ciphertext,encryption_time,plaintext,decryption_time):
    print('------------------------------------------- Original Text --------------------------------------------\n')
    print(f'Original Text:\n\n {originaltext}')
    print('\n----------------------------------------- Encryption -----------------------------------------------\n')
    print(f'\u2022Cipher Text:\n\n{ciphertext}\n')
    print(f'\u2022Encryption Time:  {encryption_time} seconds')
    print('\n----------------------------------------- Decryption -----------------------------------------------\n')
    print(f'\u2022Decrypted Text:\n\n{plaintext}')
    print(f'\u2022Decryption Time:  {decryption_time} seconds')
    print('--------------------------------------------------------------------------------------------------------')
