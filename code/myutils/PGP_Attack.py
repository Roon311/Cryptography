import PGP as pgp 

#--------------------------Create Oracle------------------------------------#
def openpgp_integrity_oracle(ciphertexttocheck,key):
    prefix=pgp.decryptor(key,ciphertexttocheck,oracle=True)
    if prefix[14:16]==prefix[16:18]:
        print(prefix)
        return 1
    else:
        return 0
#--------------------------Prepare the Ciphertext------------------------------------#
def prepareCipher(ciphertext):
    C={} #Dictionary to place the ciphertext
    counter=3 # counter to fill in the dictionary using while loop
    BS=16 #Block size
    C1 = ciphertext[0:BS] 
    C2=ciphertext[BS:18] 
    C[1]=C1#C1 in dict
    C[2]=C2#C2 in dict
    print(len(C1))
    print(len(C2))
    ciphertext=ciphertext[18:] #set the ciphertext from after c2
    while ciphertext:
        data=ciphertext[:BS]
        C[counter]=data
        ciphertext=ciphertext[BS:]
        counter+=1
    return C,C1,C2
#--------------------------Divide the Message------------------------------------#
def divideMsg(plaintext):
    counter=1# counter to fill in the dictionary using while loop
    BS=16#Block size
    msgDivided={}#msg dict
    while plaintext:
        plaindata=plaintext[:BS]
        msgDivided[counter]=plaindata
        plaintext=plaintext[BS:]
        counter+=1
    return msgDivided
#---------------------------------------------------------------------------------#
def stopper(index):
    if index==10:
        return True
#-------------------------Find First Rune------------------------------------------#
def findFirstTwo(key,ciphertext,E_k0_b,index):
    assert index>=1
    C,_,_=prepareCipher(ciphertext)#get the ciphertext ready
    D=iv=b'\x00' * (16)# Let D be a 2 byte integer representing 0
    C_dash2=[]#C dash that will be formed
    C_dash2.append(C[index+2]) #append C that has the index+2
    C_dash2.append(D) #put the D
    values2 = [value for key, value in C.items() if key >= 3]#get from C3 in a list
    C_dash2.extend(values2)#([C1]3−b||C2, D, C3, C4, . . .).
    #print(len(C_dash2))
    x=0
    C_dash_string2 = b''.join(C_dash2)#turn into a single byte string
    x=openpgp_integrity_oracle(C_dash_string2,key)
    while x!=1: #if not valid cipher
        #print(D)
        D = int.from_bytes(D, byteorder='big') +1 #increment the d by 1 
        D = D.to_bytes(2, byteorder='big') #convert back to bytes
        C_dash2[1]=D #change the value of D in the list
        C_dash_string2 = b''.join(C_dash2)#convert the list to single byte string
        x=openpgp_integrity_oracle(C_dash_string2,key)#call the oracle
    Cib_b1=C[index+2][14:16]
    #apply the equations
    temp=bytes([f ^ b for f, b in zip(Cib_b1,D)])
    EkCiplus2=bytes([f ^ b for f, b in zip(temp,E_k0_b)])
    Miplus1=bytes([f ^ b for f, b in zip(EkCiplus2,C[index+3][0:2])])
    return Miplus1
#original text
originaltext=b'I Hate You Buddy :3 Yours Omar hiiiiiiiiiiiiiiiiiiiiiiiiiii y\xce\xbb\x028\xd3p_5|\x9b\xb6\xf6\xf9?\xfe\xbdf\x9a\xde~\x052\x92\x89l\xd4$\xdeK\xbc\xef\x0fXq)N1\xbf\x18\x04|Bo\x89\xf8\xb9\x94b\x95D\x05&L\xaa\\!8\x0b\xd1\xec\xdc\xa6X4\x8c\x89\x90Y\x02<\xa2\xc2:`\x1b8 V\xaeYh\xcf\xa6\x19)\xd7r_\x14,'
#ciphertext
ciphertext=b"\xee\x19\xe55\xb0v\x8f\x86\xff$65\x13>R\xa6'aH\x92\xbe2\xe2\xc4\x16\x8c\x06\xa7_\xfc\xc0|\x1f\xb3i>\xd1b2\xe7/\x8ad\\PU\xb5\x80\x97\x96y\xff\xa5k\ti+\x80\xf7d\xc8\xaeq\xf9\x91\xa4\xea\x07\x9a6P[\x0c\xe6\x8e\x13\x1d\xd5\r\x81U8\t\xa7\xde\x9f\xe7\x8ab\xbd\x8da\x00B\xf0\xac\x82\x8aH~U\xa8,s\x99\x83\xbaz\x00>\xc1\xc6\xdc\xd7\x0b[Mp\x98\x8f\xef\x86)u\xfd\xf3\xe4u\xd6\xdfW\x88\xc56\xfa\xf0(\xb6\xfeC\xf0UD\xc3\xac\xa8\x84\xb6|\x1a\xc0\x00\x08\xe8\\\x8b3}^~\xc8\x9b\x03\xef\xfbe\xa8\xc7\xd5"


plaintext=originaltext
C,C1,C2=prepareCipher(ciphertext)#get the ciphertext ready in dict

D=0
D = D.to_bytes(2, byteorder='big')
C_dash=[]
C_dash.append(C1[2:16]+C2) #C' = ([C1]3−b||C2, D, C3, C4, . . .)
print(C1)
print(C2)
print(C_dash)
C_dash.append(D)
values = [value for key, value in C.items() if key >= 3]
C_dash.extend(values)
C_dash_string = b''.join(C_dash)
keyy=b'\x10#\x90\x00\xff\x00\x01\x10\x00\r\xc6\x00\xd0\x0f\xff\x08'

x=openpgp_integrity_oracle(C_dash_string,keyy)

while x==0:
    #print(D)
    D = int.from_bytes(D, byteorder='big') + 1#increment the d by 1 
    D = D.to_bytes(2, byteorder='big')#convert back to bytes
    C_dash[1]=D#change the value of D in the list
    C_dash_string = b''.join(C_dash)#convert the list to single byte string
    x=openpgp_integrity_oracle(C_dash_string,keyy)#call the oracle

msgDivided=divideMsg(originaltext)#get the message dict ready
e_1_2 = bytes([f1 ^ c1 for f1, c1 in zip(C[3][:2],b'I ')])#get EK([C1]3−b||C2) 
E_k0_b=bytes([f ^ b ^ cc for f, b, cc in zip(C[2],e_1_2,D)])
D = int.from_bytes(D, byteorder='big') 
print('D value:',D)
print(E_k0_b)

index=1#set start index
while index<len(C):
    Miplus1=findFirstTwo(keyy,ciphertext,E_k0_b,index)#get first 2 bytes
    #Compare
    print('----------------------------------------------------------------------')
    print('Expected Output: ',msgDivided[index+1][0:2])
    print('Actual Output:   ',Miplus1)
    print('----------------------------------------------------------------------')

    index+=1 #increment the index
    if(stopper(index)==True): break #stop not to take time
