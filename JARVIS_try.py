import pyttsx3 as pyt
import speech_recognition as sr
import datetime as dt
import os
import wikipedia
import webbrowser
import pywhatkit
import requests
from bs4 import BeautifulSoup
from googlesearch import search

engine = pyt.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hr = int(dt.datetime.now().hour)
    if(hr>=0 and hr<12):
        speak("Kaalai Vanakkam !!")
    elif(hr>=12 and hr<18):
        speak("Vannakam !!")
    elif(hr>=18 and hr<20):
        speak("Maaalai Vannakam !!")
    speak("Naan dhaaan Nelson, ungalukku enna venum?")

def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        speak("listening")
        print("Listening....")
        audio = rec.listen(source)
    try:
        print("Recognizing...")
        query = rec.recognize_google(audio,language='en-in')
        query = query.lower()
        print("You said:", query ,"\n")
    except Exception as e:
        speak("say that again please")
        print("Say that again please")
        return "None"
    return query

#launch system apps
def app(appname):
    speak('opening '+ appname)
    appname = appname.replace(" ","")
    os.system(appname)

#open websites
def website(site):
    speak("opening website "+ site)
    site = site.replace(" ","")
    webbrowser.open("www."+site+".com")

#watch youtube videos
def youtube(video):
    speak("Opening youtube "+ video)
    pywhatkit.playonyt(video)

def google_scearch(ques):
    query = ques
    for j in search(query,tld="co.in",num=10,stop=10,pause=2):
        return(j)


def weather():
    city = "lucknow"
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    string = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = string.split('\n')
    time = data[0]
    sky = data[1]
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    pos = strd.find('Wind')
    other_data = strd[pos:]
    print("Temperature is", temp)
    print("Time: ", time)
    print('Sky Description:', sky)
    speak("Temperature is "+ temp)
    speak("The sky is"+ sky)

#main
if __name__ == "__main__":
    greet()
    while True:
        query=listen().lower()

        if "time" in query:
            now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(now)
            speak(now)

        elif "weather" in query:
            weather()
        
        #launch keyword to launch system apps
        elif "launch" in query:
            appname = query[7:]
            print(appname)
            app(appname)

        elif "open easwari" in query:
            webbrowser.open("https://ai.srmeaswari.ac.in/")    

        elif "open uv" in query:
            webbrowser.open("https://theuvofearth.wixsite.com/stage1")

        #open keyword to open websites
        elif "open" in query:
            site = query[5:]
            website(site)

        #watch keyword to search and watch youtube videos
        elif "watch" in query:
            utube = query[6:]
            youtube(utube)

        elif "search" in query: #returns the best website for asked query
            try:
                result = query[6:]
                speak("giving best results for"+ result)
                google_scearch(result)
                webbrowser.open(google_scearch(result))
            except:
                print("please say something after search")
                speak("please say something after search")