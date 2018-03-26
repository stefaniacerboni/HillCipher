import numpy as np
import fractions as frac
import random
import algmod


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
dic = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
       'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
       'Z': 25}


def generate_key(m):
#Crea una matrice di numeri casuali fino a che il determinante non e' coprimo con 26 (matrice invertibile)
    coprime = False
    while coprime is False:
        K = np.zeros(shape=(m, m))
        for i in range(m):
            for j in range(m):
                K[i][j] = random.randint(0,25)
        det = int(round(np.linalg.det(K) % 26))
        if frac.gcd(det, 26) == 1:
            coprime = True
    print(str(K))
    stringkey = ''
    for i in range(m):
        for j in range(m):
            stringkey += letters[int(K[i][j])]
    print("As string, the key is: "+stringkey)
    return K


def hill_encryption(m, plaintext, key):
#Dato un plaintext e la dimensione m dei blocchi (conosciuta a priori), cripta il messaggio usando una chiave generata
#casualmente e che verra' comunicata all'utente insieme al relativo ciphertext alla fine del procedimento
    Pstar = np.zeros(shape=(m, len(plaintext)/m))
    Cstar = np.zeros(shape=(m, len(plaintext)/m))
    ciphertext = ''
    k = 0
    for j in range(len(plaintext)/m):
        for i in range(m):
            Pstar[i][j] = dic[plaintext[k]]
            if k >= len(plaintext):
                break
            else:
                k += 1
    for j in range(len(plaintext)/m):
        a = Cstar[:,j]
        Cstar[:,j] = algmod.modmatmul(key, Pstar[:,j])
    for j in range(len(plaintext)/m):
        for i in range(m):
            ciphertext += letters[int(Cstar[i,j])]
    print(ciphertext)
    return ciphertext


def hill_decryption(ciphertext, K):
#Dato un ciphertext e la chiave, ricava il messaggio in chiaro calcolando la matrice inversa della chiave ed applicandola
#al ciphertext, ottenendo cosi' il plaintext
    plaintext = ''
    m = K.shape[0]
    detK = int(round(np.linalg.det(K) % 26))
    inverseK = algmod.modular_inverse(K, detK)
    Pstar = np.zeros(shape=(m, len(ciphertext)/m))
    Cstar = np.zeros(shape=(m, len(ciphertext)/m))
    k=0
    for j in range(len(ciphertext)/m):
        for i in range(m):
            Cstar[i][j] = dic[ciphertext[k]]
            if k >= len(ciphertext):
                break
            else:
                k += 1
    for j in range(len(ciphertext)/m):
        a = Pstar[:,j]
        Pstar[:,j] = algmod.modmatmul(inverseK, Cstar[:,j])
    for j in range(len(ciphertext)/m):
        for i in range(m):
            plaintext += letters[int(Pstar[i,j])]
    print(plaintext)

def hill_attack(m, plaintext, ciphertext):
#Prova ad attaccare il cifrario conoscendo una coppia di plaintext e ciphertext e la dimensione dei blocchi.
#Potrebbe non riuscire nell'intento se la lunghezza di plaintext (e relativo ciphertext) e' troppo ridotta, in tal caso
#e' necessario recuperare piu' coppie di testo in chiaro e messaggio cifrato.

    length = len(plaintext)
    coprime = False
    Pstar = np.zeros(shape=(m, m))
    Cstar = np.zeros(shape=(m, m))
    k = 0
    plainlist = np.zeros(shape=(m,len(plaintext)/m))
    cipherlist = np.zeros(shape=(m,len(ciphertext)/m))
    det = 0
    for j in range(length / m):
        for i in range(m):
            plainlist[i][j] = dic[plaintext[k]]
            cipherlist[i][j] = dic[ciphertext[k]]
            k+=1

    for i in range(length / m):
        if coprime is False:
            k=1
            for j in range(i,(length / m) - m ):
                temp = plainlist[:,i:m + j:k]
                k+=1
                det = int(round(np.linalg.det(temp) % 26))
                if frac.gcd(det, 26) == 1:
                    coprime = True
                    Pstar = plainlist[:, i:m + j:k-1]
                    Cstar = cipherlist[:, i:m + j:k-1]
                    break
    if coprime:
        print('Matrice invertibile')

        inverse = algmod.modular_inverse(Pstar, det)
        K = algmod.modmatmul(Cstar, inverse)
        print "Chiave K: \n" + str(K)
    else:
        print('Unable to find the key')
