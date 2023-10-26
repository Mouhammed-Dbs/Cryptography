# ////////////////////////////////////////////////////////
# //        Filter Method For PlainText & Key          //
# //////////////////////////////////////////////////////

def getAlpha(text):
    t = ""
    for i in text:
        if not i.isalpha():
            if i != " ":
                return None
        else:
            t+=i.lower()
    return t

# ////////////////////////////////////////////////////////
# //        ONE TO ONE:: ADDITTIVE CIPHER              //
# //////////////////////////////////////////////////////

def add(text, k, decrypt=False):
    if getAlpha(k) == None:
        return None
    text = getAlpha(text)
    k = ord(k)-97
    if decrypt:
        k = k * -1
    outtext = ''
    for i in text:
        e = ord(i)-97+k
        if e >= 26:
            e = e -26
        if e < 0:
            e = 26 + e
        outtext += chr(ord(i)+k)
    return outtext 
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
    if getAlpha(k) == None:
        return None
    text = getAlpha(text)
    k = ord(k)-97
    if gcd(26, k) == 1:
        if decrypt:
            k = ext_gcd(26,k)
        cipherText = ""
        for i in text:
            e = (ord(i)-97)*k
            if e >= 26:
                e = e % 26
            cipherText += chr(e + 97)
        return cipherText
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
            return cipher
        return None

# print(affine("carissofast", "h", "c"))
# print(affine("qcrgyywlcyf", "h", "c", decrypt=True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY:: AUTOKEY CIPHER              //
# //////////////////////////////////////////////////////

def autokey(text, k, decrypt=False):
    if getAlpha(k) == None:
        return None
    text = getAlpha(text)
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
    return outText 
# print(autokey("attakistodaywastoodanger", "m"))
# print(autokey("mtmtksalhrdyuwslhcrdntkv", "m", decrypt=True))

# ////////////////////////////////////////////////////////
# //         ONE TO MANY:: Playfair CIPHER              //
# //////////////////////////////////////////////////////


def playfair(text, k):
    if getAlpha(k) == None:
        return None
    text = getAlpha(text)
    k = getAlpha(k)
    # init key
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
    bi_matrix = []
    bi_cipher_matrix = []
    for i in range(len(text)):
        if(i%2==0):
            if text[i+1] == text[i]:
                text = text[:i+1] + "x" + text[i+1:]
    if len(text)%2 !=0:
        text = text + "z"
    print(text)
    for i in range(0,len(text)//2):
        bi_matrix.append((text[i*2], text[i*2+1]))
    for i in bi_matrix:
        a = ''
        b = ''
        xa = -1
        ya = -1
        xb = -1
        yb = -1
        for ij,j in enumerate(matrix_key):
            if i[0] in j:
                xa = ij
                ya = j.index(i[0])
            if i[1] in j:
                xb = ij
                yb = j.index(i[1])
        if xa == xb:
            if ya!=4 and yb!=4:
                a = matrix_key[xa][ya+1]
                b = matrix_key[xb][yb+1]
            else:
                if ya == 4:
                    a = matrix_key[xa][0]
                if yb == 4:
                    b = matrix_key[xb][0]
        elif ya == yb:
            if xa!=4 and xb!=4:
                a = matrix_key[xa+1][ya]
                b = matrix_key[xb+1][yb]
            else:
                if xa == 4:
                    a = matrix_key[0][ya]
                if xb == 4:
                    b = matrix_key[0][yb]
        else:
            if xa < xb:
                a = matrix_key[xa][yb]
                b = matrix_key[xb][ya]
            else:
                a = matrix_key[xa][yb]
                b = matrix_key[ya][xb]
        bi_cipher_matrix.append((a,b))
            

    return "".join(["".join(y) for y in bi_cipher_matrix]).upper()
print(playfair("hello","lgdbaqmhecurnifxvsokzywtp"))
