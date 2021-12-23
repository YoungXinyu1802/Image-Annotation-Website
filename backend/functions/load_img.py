import base64
import os
imgs = os.listdir('bee')
print(imgs)
imgNum = len(imgs)
print(imgNum)
b64 = []
for img in imgs:
    f = open('bee/' + img, 'rb')
    res = f.read()
    s = base64.b64encode(res)
    b64.append(s)
    f = open('hello.txt', 'w')
    sb64=str(s)[2 : len(str(s)) - 1]
    f.write(str(sb64))
print(b64)

