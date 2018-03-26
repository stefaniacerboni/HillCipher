import numpy as np
import functions
import string


def __main__():
    usr_interface()
    return 0

#Semplice interfaccia di input-output con l'utente, in cui si controlla che i dati inseriti siano conformi a quelli
#che il programma si aspetta
def usr_interface():
    print('Hello user!')
    option = -1
    while option != 0 and option !=1 and option !=2:
        option = int(raw_input("Please enter 0 to encrypt a message, 1 to decrypt a message, 2 to execute an attack to hill cipher: "))
    if option == 0:
        kplaintext = str(raw_input("Please enter a plaintext to encrypt (NO numbers): ")).upper().translate(None,
                                                                                                          string.punctuation).translate(
            None, " ").translate(None, "\n")
        m = int(raw_input("Please enter block length m: "))
        #se il plaintext non e' divisibile in blocchi di dimensione m, trova il fattore minimo per cui e' divisibile
        #se la lunghezza del plaintext e' un numero primo maggiore di 10 o ha un divisore >10, il messaggio viene troncato
        if len(kplaintext) % m != 0 and len(kplaintext) < 10:
            oldm = m
            for i in (2, 3, 5, 7, 9):
                if len(kplaintext) % i == 0:
                    m = i
                    break
            print('Unable to encrypt using ' + str(oldm) + ' as block length, changing it to: ' + str(m))
        key = functions.generate_key(m)
        functions.hill_encryption(m, kplaintext, key)
    elif option == 1:
        kciphertext = str(raw_input("Please enter a ciphertext to decrypt (NO numbers): ")).upper().translate(None,
                                                                                                          string.punctuation).translate(
            None, " ").translate(None, "\n")
        m = int(raw_input("Please enter block length m: "))
        stringkey = str(raw_input("Please enter Key (as characters): ")).upper().translate(None,
                                                                                                          string.punctuation).translate(
            None, " ").translate(None, "\n")
        key = np.zeros(shape=(m, m))
        z = 0
        for i in range(m):
            for j in range(m):
                key[i][j] = functions.dic[stringkey[z]]
                if z >= len(stringkey):
                    break
                else:
                    z += 1
        functions.hill_decryption(kciphertext, key)
    elif option == 2:
        kciphertext = str(raw_input("Please enter the ciphertext (NO numbers): ")).upper().translate(None,
                                                                                                          string.punctuation).translate(
            None, " ").translate(None, "\n")
        kplaintext = str(raw_input("Please enter the plaintext (NO numbers): ")).upper().translate(None,
                                                                                                          string.punctuation).translate(
            None, " ").translate(None, "\n")
        m = int(raw_input("Please enter block length m: "))
        functions.hill_attack(m, kplaintext, kciphertext)




if __name__ == __main__():
    __main__()
