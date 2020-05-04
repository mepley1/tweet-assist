#!/usr/bin/env python3

from tkinter import *
import requests
import tweepy
from datetime import datetime #for logging
import pickle

def sendtweet():
    try:
        tweet = str(T.get('1.0', END))
        # authenticate
        auth = tweepy.OAuthHandler(e1.get(), e2.get())
        auth.set_access_token(e3.get(), e4.get())        
        api = tweepy.API(auth)
        api.update_status(tweet)
    except Exception as e:
        print('Error - Tweet not sent:')
        logerror(e)
        return
    info('Tweet sent', 1)
    logTweet(tweet)

def logerror(message):
    File_object = open(r'errorlog.txt', 'a')
    File_object.write(str(datetime.now()) + '\n' + str(message) + '\n' + 'Not posted: ' + str(T.get('1.0', END)) + '\n')
    File_object.close()
    info(message, 0)    

def logTweet(z):
    File_object = open(r'tweets.txt', 'a')
    File_object.write(str(datetime.now()) + ' Tweeted:' + '\n' + z + '\n')

def clearEntries():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

def saveKeys():
    keys = [str(e1.get()), str(e2.get()), str(e3.get()), str(e4.get())]
    pickle.dump(keys, open('auth.dat', 'wb'))

def loadKeys():
    try:
        keys = pickle.load(open('auth.dat', 'rb'))
        clearEntries()
        e1.insert(END, keys[0])
        e2.insert(END, keys[1])
        e3.insert(END, keys[2])
        e4.insert(END, keys[3])
        info('Found saved keys', 1)
    except Exception as e:
        print(e)
        info('No saved keys found', 0)

def checkConnection():
    try:
        r = requests.head('https://twitter.com')
        result = str(r)
        if result:
            tester(1)
            return
    except requests.exceptions.RequestException as e:
        tester(0)

def tester(w):
    if w:
        Testerthing.config(text='Connection OK', bg='green', fg='white')
    else:
        Testerthing.config(text='Connection failed, test again?', bg='#b00000', fg='white')

beencleared = False

def clearo(*args):
    global beencleared
    if beencleared:
        return
    else:
        T.delete('1.0', END)
        beencleared = True

def info(x, c):
    if c:
        color = '#1DA1F2'
    else:
        color = 'red'
    Help.config(text=x, fg=color)

# gui
print('making gui...')
root = Tk()
root.resizable(True, True)
root.maxsize(420,1024)
root.grid_columnconfigure(0, weight=1, uniform=1)
root.grid_columnconfigure(1, weight=1, uniform=1)
root.title('Tweep assistant')

Label(root, text="API key:").grid(row=0, sticky=W)
Label(root, text="API secret:").grid(row=1, sticky=W)
Label(root, text="Access token:").grid(row=2, sticky=W)
Label(root, text="Access token secret:").grid(row=3, sticky=W)

e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root)
e4 = Entry(root)

e1.grid(row=0, column=1, sticky=EW)
e1.config(show='*')
e2.grid(row=1, column=1, sticky=EW)
e2.config(show='*')
e3.grid(row=2, column=1, sticky=EW)
e3.config(show='*')
e4.grid(row=3, column=1, sticky=EW)
e4.config(show='*')

T = Text(root, height=10, font='sans', bg='#FFFFFF', fg='#000000')
T.bind('<Button-1>', clearo)
T.grid(row=4, column=0, sticky=EW, columnspan=2)
T.insert(END, 'Type your tweet here.')

Button(root, text='Send Tweet!', command=sendtweet, bg='#1DA1F2', fg='#FFFFFF').grid(row=5, column=0, sticky=EW, columnspan=2)
Button(root, text='Save keys', command=saveKeys).grid(row=6, column=0, sticky=EW)
Button(root, text='Reload keys', command=loadKeys).grid(row=6, column=1, sticky=EW)
Testerthing = Button(root, text='Check connection', command=checkConnection)
Testerthing.grid(row=7, column=0, sticky=EW, columnspan=2)
Help = Label(root, text='https://epley.me', fg='#1DA1F2')
Help.grid(row=8, column=0, sticky=E, columnspan=2)

# load keys on start if a save exists
try:
    loadKeys()
except Exception as e:
    print(e)

root.mainloop()
