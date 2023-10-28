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
    if getAlpha(k) == None:
        return None
    text = getAlpha(text)
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
    text = getAlpha(text)
    k = getAlpha(k)
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
print(playfair("hello","lgdba qmhec urnif xvsok zywtp"))
print(playfair("ECQZBX","lgdba qmhec urnif xvsok zywtp", decrypt=True))

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
    text = getAlpha(text)
    k = getAlpha(k)
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
print(vigenere('she is listening', 'pascal'))
print(vigenere('HHWKSWXSLGNTCG', 'pascal', True))

