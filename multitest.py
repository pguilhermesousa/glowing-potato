import base64
import sys
import imgurAPIrequests
import requests
import time
from AesEverywhere import aes256
from stegano import lsb
from bs4 import BeautifulSoup
from threading import Thread


def uploadFunction(imgOriginal, imgSecret, room):
    tsStart = time.time()
    imageOriginal = imgOriginal
    imageSecret = imgSecret

    mainUrl = "http://dontpad.com/"
    room = room

    secretMessage = "MCyber"
    password = "MCyber"

    encrypted = aes256.encrypt(secretMessage, password)
    enc = encrypted.decode("utf-8")

    secret = lsb.hide(imageOriginal, enc)
    secret.save(imageSecret)

    imageName = "testImage"
    imageTitle = "Test"

    with open(imageSecret, "rb") as secretImage:
        data = base64.b64encode(secretImage.read())
        result = imgurAPIrequests.uploadImageAnonymous(data, imageName, imageTitle)

    url = mainUrl + room
    payload = {"text": result}
    req = requests.put(url, data=payload)

    tsEnd = time.time()
    tsDiff = tsEnd - tsStart
    print(tsDiff)

def downloadFunction(room):
    tsStart = time.time()
    mainUrl = "http://dontpad.com/"
    room = room

    response = requests.get(mainUrl + room)
    html = response.text
    soup = BeautifulSoup(html, features='html.parser')
    imageUrl = soup.find("textarea", {"id": "text"}).get_text()

    image = requests.get(imageUrl).content

    x = imageUrl.split("/")
    filename = x[3]
    with open(filename, "wb") as handler:
        handler.write(image)

    password = "MCyber"
    message = lsb.reveal(filename)
    decrypted = aes256.decrypt(message, password)
    secretMessage = decrypted.decode("utf-8")
    print(secretMessage)

    tsEnd = time.time()
    tsDiff = tsEnd - tsStart
    print(tsDiff)


t1 = Thread(target=uploadFunction("original/big.png", "testingwithhal1"))
t2 = Thread(target=uploadFunction("original/medium.png", "testingwithhal2"))
t3 = Thread(target=uploadFunction("original/small.png", "testingwithhal3"))

t1.start()
t2.start()
t3.start()
