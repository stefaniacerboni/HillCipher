import numpy as np

#trova la matrice inversa di A modulo 26, dato il suo determinante (che controlla essere coprimo con 26)
def modular_inverse(A, detA):
    m = len(A)
    inverse = np.zeros(shape=(m, m))
    detminus1 = mulinv(detA, 26)
    for i in range(m):
        for j in range(m):
            newA = getsubmatrix(A, j, i)
            det1 = np.linalg.det(newA)
            inverse[i][j] = ((-1) ** (i + j) * detminus1 * det1) % 26
    return inverse


#Applicazione dell'algoritmo di euclide esteso per trovare l'inverso moltiplicativo di un numero modulo 26


def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def mulinv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n

#ottiene la sottomatrice togliendo ad A la riga i e la colonna j
def getsubmatrix(A, noti, notj):
    newA = np.delete(np.delete(A, noti, 0), (notj), 1)
    return newA


#esegue la moltiplicazione tra matrici (o tra matrice e vettore, gestito nel caso in cui la dimensione delle colonne
#sia unitaria) modulo 26
def modmatmul(A, B):
    rows = A.shape[0]
    try:
        col = (B.shape[1])
        res = np.zeros(shape=(rows, col))
    except IndexError:
        col = 1
        res = np.zeros(shape=(rows,))

    if col == 1:
        for i in range(rows):
            res[i] = int(round(np.dot(A[i, :], B))) % 26
    else:
        for i in range(rows):
            for j in range(col):
                a = A[i, :]
                b = B[:, j]
                res[i][j] = int(round(np.dot(A[i, :], B[:, j]) % 26))
    return res

