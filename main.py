# ////////////////////////////////////////////////////////
# //        Filter Method For PlainText & Key          //
# //////////////////////////////////////////////////////

def validText(text, isDigit=False):
    t = ""
    for i in text:
        if not i.isalpha():
            if isDigit and i.isdigit():
                t+=i.lower()
                continue
            if i != " ":
                return None
        else:
            t+=i.lower()
    return t

# ////////////////////////////////////////////////////////
# //        ONE TO ONE:: ADDITTIVE CIPHER              //
# //////////////////////////////////////////////////////

def add(text, k, decrypt=False):
    if validText(k) == None:
        return None
    text = validText(text)
    k = ord(k)-97
    if decrypt:
        k = k * -1
    outText = ''
    for i in text:
        e = ord(i)-97+k
        if e >= 26:
            e = e -26
        if e < 0:
            e = 26 + e
        outText += chr(ord(i)+k)
    if decrypt: return outText
    return outText.upper()
# print(add('aliisstrongman', 'c'))
# print(add('cnkkuuvtqpiocp','c',True))

# ////////////////////////////////////////////////////////
# //       ONE TO ONE:: MULTIPLICATIVE CIPHER          //
# //////////////////////////////////////////////////////

def gcd(r1, r2):
    r = 0
    while(r2>0):
        r = r1 % r2
        r1 = r2
        r2 = r
    return r1

def ext_gcd(r1, r2):
    r = 0
    t = 0
    t1 = 0
    t2 = 1
    while(r2>0):
        q = r1 // r2
        r = r1 -q*r2
        r1 = r2
        r2 = r
        t = t1 -q*t2
        t1 = t2
        t2 = t
    if(r1 == 1):
        if(t1>0):
            return t1
        else:
            return 26 + t1

def multi(text, k, decrypt=False):
    if validText(k) == None:
        return None
    text = validText(text)
    k = ord(k)-97
    if gcd(26, k) == 1:
        if decrypt:
            k = ext_gcd(26,k)
        outText = ""
        for i in text:
            e = (ord(i)-97)*k
            if e >= 26:
                e = e % 26
            outText += chr(e + 97)
        if decrypt: return outText
        return outText.upper()
    else:
        return None
# print(multi("car is so fast", "h"))
# print(multi("oapewwujawd", "h", decrypt=True))

# /////////////////////////////////////////////////////////
# //         ONE TO ONE:: AFFINE CIPHER                 //
# ///////////////////////////////////////////////////////

def affine(text, k1, k2, decrypt=False):
    if decrypt:
        c = add(text, k2, decrypt=True)
        plain = multi(c, k1, decrypt=True)
        return plain
    else:
        cipher1 = multi(text, k1)
        if cipher1 != None:
            cipher = add(cipher1, k2)
            return cipher.upper()
        return None

# print(affine("carissofast", "h", "c"))
# print(affine("qcrgyywlcyf", "h", "c", decrypt=True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY:: AUTOKEY CIPHER              //
# //////////////////////////////////////////////////////

def autokey(text, k, decrypt=False):
    if validText(k) == None:
        return None
    text = validText(text)
    k = ord(k)-97
    if decrypt:
        k = k * -1 
    outText = ''
    for c in text:
        e = ord(c)-97+k
        if e >= 26:
            e = e - 26
        if e < 0:
            e = 26 + e
        outText += chr(e+97)
        if decrypt:
            k = -e
        else:
            k = ord(c)-97
    if decrypt: return outText
    return outText.upper()
# print(autokey("attakistodaywastoodanger", "m"))
# print(autokey("mtmtksalhrdyuwslhcrdntkv", "m", decrypt=True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY:: Playfair CIPHER             //
# //////////////////////////////////////////////////////

def getMatrixKey(k):
    matrix_key = [[],[],[],[],[]]
    lk = []
    for i in k.lower():
        if i == 'j':
            i = 'i'
        if i not in lk:
            lk.append(i)
    if len(lk) != 25:
        for i in range(97, 123):
            if i == 106:
                continue
            if chr(i) not in lk:
                lk.append(chr(i))
    for i in lk:
        for j in matrix_key:
            if len(j)==5:
                continue
            else:
                j.append(i)
                break
    return matrix_key
def eF(x):
    if x>4:
        return 0
    if x<0:
        return 4
    return x

def clearPadding(text):
    for i in range(len(text)):
        if i < len(text):
            if text[i] == 'x' and i != 0 and i != len(text)-1:
                if text[i-1] == text[i+1]:
                    text = text[:i] + text[i+1:]
    if len(text) % 2 !=0 and text[-1] == 'x':
        text = text[:-1]
    return text

def playfair(text, k, decrypt=False):
    text = validText(text)
    k = validText(k)
    if k == None or text == None:
        return None
    # init key
    matrix_key = getMatrixKey(k)

    # init bi_matrix
    bi_matrix = []
    for i in range(len(text)-1):
        if(i%2==0):
            if text[i+1] == text[i]:
                text = text[:i+1] + "x" + text[i+1:]
    if len(text)%2 !=0:
        text = text + "x"
    for i in range(0,len(text)//2):
        bi_matrix.append((text[i*2], text[i*2+1]))

    # plainfair algorithm
    f = 1
    if decrypt:
        f = -f
    bi_out_matrix = []
    for i in bi_matrix:
        a = ''
        b = ''
        ai = [-1, -1]
        bi = [-1, -1]
        for ij,j in enumerate(matrix_key):
            if i[0] in j:
                ai[0] = ij
                ai[1] = j.index(i[0])
            if i[1] in j:
                bi[0] = ij
                bi[1] = j.index(i[1])
        if ai[0] == bi[0]:
            a = matrix_key[ai[0]][eF(ai[1]+f)]
            b = matrix_key[bi[0]][eF(bi[1]+f)]
        elif ai[1] == bi[1]:
            a = matrix_key[eF(ai[0]+f)][ai[1]]
            b = matrix_key[eF(bi[0]+f)][bi[1]]
        else:
            a = matrix_key[ai[0]][bi[1]]
            b = matrix_key[bi[0]][ai[1]]
        bi_out_matrix.append((a,b))
    outText = "".join(["".join(y) for y in bi_out_matrix])
    if decrypt: return clearPadding(outText)
    return outText.upper()
# print(playfair("hello","lgdba qmhec urnif xvsok zywtp"))
# print(playfair("ECQZBX","lgdba qmhec urnif xvsok zywtp", decrypt=True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY:: VIGENERE CIPHER             //
# //////////////////////////////////////////////////////

def initKey(text, k):
    st = len(text)
    sk = len(k)
    q = -1
    r = -1
    if st > sk:
        q = st // sk
        r = st % sk
        k = k * q
        for i in range(r):
            k += k[i]
    elif st < sk:
        k = k[:len(text)]
    return k
        
def vigenere(text, k, decrypt=False):
    text = validText(text)
    k = validText(k)
    if text == None or k == None:
        return None
    k = initKey(text, k)
    f = 1
    if decrypt:
        f = -f
    outText = ''
    for i in range(len(text)):
        e = ord(text[i]) - 97 + (f * (ord(k[i])-97))
        if e < 0: e = 26 + e
        if e > 26: e = e - 26
        outText += chr(e + 97)
    if decrypt: return outText
    return outText.upper()
# print(vigenere('she is listening', 'pascal'))
# print(vigenere('HHWKSWXSLGNTCG', 'pascal', True))

# one-time pad (OTP) conditions:
# key is random and use for one time
# len(key) = len(text)

# print(vigenere('she is listening aj so ss', 'sjlbacbvvbsocdjbadkba'))
# print(vigenere('KQPJSNJNOFFWPJJKSRCT', 'sjlbacbvvbsocdjbadkba', True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY::  ADFGVX CIPHER              //
# //////////////////////////////////////////////////////

import math
def padding(text, k):
    if len(text) % len(k) != 0:
        pading = 'A'
        pading = pading * ( (len(k) - (len(text) % len(k))) )
        text = text + pading
    return text

def convertBi(text, k1, k2, decrypt=False):
    word = 'adfgvx'
    outText = ""
    if decrypt:
        for i in range(0, len(text), 2):
            if i == len(text)-1: break
            r = word.index(text[i])
            c = word.index(text[i+1])
            outText += k1[r*6 + c]
    else:
        for ch in text:
            r = k1.index(ch) // 6
            c = (k1.index(ch) % 6)
            outText += word[r]+word[c]
        outText = padding(outText, k2)
    return outText

def convertSort(text, k, decrypt=False):
    outText = ""
    if decrypt:
        s_text = math.ceil(len(text) / len(k))
        d = {}
        ka = "".join(sorted(k))
        for i in range(len(k)):
            d[ka[i]] = text[i*s_text:s_text*(i+1)]

        text_sort_key = ""
        for i in range(len(d)):
            text_sort_key += d[k[i]]
        outText = ""
        for i in range(s_text):
            for j in range(len(k)):
                outText += text_sort_key[j * s_text + i]
        return outText
    else:
        s_text = math.ceil(len(text) / len(k))
        last_text = ""
        for i in range(len(k)):
            for j in range(s_text):
                last_text += text[j * len(k) + i]
        d = {}
        for i in range(len(k)):
            d[ord(k[i])] = last_text[i * s_text : s_text * i + s_text]
        sorted_text = []
        for k,v in d.items():
            sorted_text.append(k)
        sorted_text.sort()
        for i in sorted_text:
            outText += d[i]
    return outText

def adfgvx(text, k1, k2, decrypt=False):
    text = validText(text, True)
    k1 = validText(k1, True)
    k2 = validText(k2)
    if text == None or k1 == None or k2 == None:
        return None
    k = [chr(i) for i in range(97,123)]+[chr(i) for i in range(49,58)]
    if(len(k1)==0):
        k1 = "".join(k)
    else:
        for c in k: 
            if c not in k1:
                k1 += c
    if decrypt:
        original_bi = convertSort(text, k2, True)
        outText = convertBi(original_bi, k1, k2, True)
        return outText
    bi_text = convertBi(text, k1, k2)
    outText = convertSort(bi_text, k2)
    return outText.upper()
# print(adfgvx('computer', 'orange', 'rinad'))
# print(adfgvx('AGXAFFAADFDAAVAADGGD', 'orange', 'rinad', True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY::  HILL CIPHER                //
# //////////////////////////////////////////////////////

import numpy as np
import math as ma

def padding(text, k):
    mod = len(text) % k.shape[1]
    if mod != 0:
        q = k.shape[1] - mod
        padding ='a'*q
        text += padding
    return text

def getRandomKey(dim):
    arr = np.random.randint(0, 27, size=(dim, dim))
    print("Getting Key....")
    while(True):
        arr = np.random.randint(0, 27, size=(dim, dim))
        det = np.linalg.det(arr)
        if det != 0 and det > 0 and ext_gcd(26, det%26) != None:
            print(arr)
            print("det:", det)
            break
        elif det != 0 and det < 0 and ext_gcd(26, 26 - (abs(det)%26)) != None:
            print(arr)
            print("det:", det)
    return arr
# getRandomKey(4)

def hill(text, k, decrypt=False):
    if k.shape[0] != k.shape[1] or np.linalg.det(k) == 0:
        return None
    text = validText(text)
    if decrypt:
        det = np.linalg.det(k)
        adj = np.linalg.inv(k) * det
        invDet = None
        if det > 0:
            invDet = ext_gcd(26, det%26)
        else:
            invDet = ext_gcd(26, 26 - (abs(det)%26))
        print(invDet)
        invK = invDet * adj
        k = invK
    else:
        text = padding(text, k)

    r = ma.ceil(len(text) / k.shape[1])
    matrix_text = np.zeros((r, k.shape[1]),dtype=int)
    for i,row in enumerate(matrix_text):
        for j,c in enumerate(row):
            matrix_text[i][j] = ord(text[i*k.shape[1] + j]) -97
    matrix_text = matrix_text.round().astype(int)
    k = k.round().astype(int)
    outMatrix = np.matmul(matrix_text, k)
    outMatrix = np.remainder(outMatrix, 26)
    outText = ""
    for i,row in enumerate(outMatrix):
        for j,c in enumerate(row):
            if c == 26: c = 0
            outText += chr(int(c)+97)
    return outText

# k = np.array([[6, 11, 20], [24, 6, 1], [9, 13, 5]])
# kk = np.array([[2, 17], [3, 14]])
# kkk = np.array([[12, 7, 12, 11], [14, 21, 25, 3], [5, 6, 19, 12], [26, 23, 5, 24]])
# print(hill('informatic', k))
# print(hill('rfodicbduuqq', k, True))
