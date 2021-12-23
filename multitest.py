import base64
import imgurAPIrequests
import requests
import time
from AesEverywhere import aes256
from stegano import lsb
from bs4 import BeautifulSoup
from threading import Thread


def uploadFunction(imgOriginal, imgSecret, room):
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


def downloadFunction(room):
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


def testFunction(imgOriginal, imgSecret, room):
    tsStart = time.time()

    uploadFunction(imgOriginal, imgSecret, room)
    downloadFunction(room)

    tsEnd = time.time()
    tsDiff = tsEnd - tsStart
    print(tsDiff)


t1 = Thread(target=testFunction("original/small.png", "smallSecret.png", "testingwithhal1"))
t2 = Thread(target=testFunction("original/medium.png", "mediumSecret.png", "testingwithhal2"))
t3 = Thread(target=testFunction("original/big.png", "bigSecret.png", "testingwithhal3"))

t1.start()
t2.start()
t3.start()
