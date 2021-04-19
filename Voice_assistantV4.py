from tkinter import *
import tkinter as tk
import string
from PIL import ImageTk, Image
from tkinter import messagebox

from pywikihow import search_wikihow
import speech_recognition as sr
import wikipedia as googleScrap
from datetime import date
import pywhatkit as kit
import webbrowser
import speedtest
import pyautogui
import requests
import datetime
import pyttsx3
import time
import os

class main():


    def __init__(self):
        # self._command_received = False

        self.screen = Tk()
        # to remove the title bar
        self.screen.overrideredirect(1)

        #==================================
        w = 320  # width for the Tk root
        h = 410  # height for the Tk root

        # get screen width and height
        ws = self.screen.winfo_screenwidth()  # width of the screen
        hs = self.screen.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.screen.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #==================================
        # self.screen.geometry('320x410')
        self.font_ = 'calibri 13 bold'
        # And Image should be in the same folder where there is script saved
        self.frame2 = PhotoImage(file='siri.gif', format="gif -index 2")

        # self.icon_ = PhotoImage(file='hangman.png')
        # Icon set for program window
        # self.screen.iconphoto(False, self.icon_)
        self.screen.title('Sound Assistant App')
        #How to make a Tkinter window not resizable?
        self.screen.resizable(False, False)

        self.frameCnt = 22
        self.frames = [PhotoImage(file='siri.gif', format='gif -index %i' % (i)) for i in range(self.frameCnt)]

        def update(ind):

            frame = self.frames[ind]
            ind += 1
            if ind == self.frameCnt:
                ind = 0
            label.configure(image=frame)
            self.screen.after(100, update, ind)

        #======================================================

        # =====================================================
        # your function is here !!!

        def speak(audio):
            engine.say(audio)
            engine.runAndWait()

            
        def _update_command(_word):
            # show_Siri()
            try:
                self.received_command.configure(text=_word)
            except:
                print('got you')


        def takeCommand():
            # It takes microphone input from the user and returns string output

            r = sr.Recognizer()
            r.pause_threshold = 1
            with sr.Microphone(device_index=10) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)

            try:
                query = r.recognize_google(audio, language='en-in')
                print(query)

            except Exception as e:
                print("Exception: 999 " + str(e))

                return "None"
            return query.lower()




        def show_Siri(_word):

            self.screen.after(5000, lambda: destroyWindow())  # Destroy the widget after 30 seconds
            self.screen.after(1000, lambda: speak(_word))  # Destroy the widget after 30 seconds
            # self.screen.after(3000, lambda: takeCommand())  # Destroy the widget after 30 seconds
            try:
                _update_command(_word)
            except:
                print('got you again')


            # let us do the trick of looping inside hangman function
            self.screen.mainloop()


        def VoiceAssistant():
            try:
                print("Listening...")
                query = takeCommand()

                if query.count(WAKE) > 0:

                    print("Listening...")
                    show_Siri('Yes..')


                # For checking internet speed
                if 'speed' in query:
                    st = speedtest.Speedtest()
                    dl = st.download()
                    ul = st.upload()
                    dl = dl / 10000000
                    dl = int(dl)
                    ul = ul / 10000000
                    ul = int(ul)
                    # print(f"The downloading speed is {dl} megabytes per second and uploading speed is {ul} megabytes per second")
                    show_Siri(f'checking internet speed, it will take couple seconds\nThe downloading speed is {dl} mbps and uploading speed is {ul} mbps')




                # Reminder
                elif 'set a reminder' in query:
                    try:
                        query = query.replace('set a reminder', '')
                        query = query.replace('for', '')
                        remember = open('data.txt', 'w')
                        remember.write(query)
                        show_Siri('reminder set')

                        remember.close()


                    except Exception as e:

                        show_Siri('Sorry, fail to set a reminder')




                elif 'reminders' in query:
                    remember = open('data.txt', 'r')
                    show_Siri(str(remember.read()))

                    remember.close


                    # self._command_received = True


                # Weather
                elif 'weather' in query:
                    api_key = "a24121fc4ed5ee71f440da2706d4b655"
                    query = query.replace("what's the", "")
                    query = query.replace("weather in", "")
                    city = query
                    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric" + "&appid=" + api_key
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        main = data['main']
                        temperature = main['temp']
                        report = data['weather']

                        show_Siri(f"{temperature} degree celsius")

                    else:
                        show_Siri("Please repeat by saying alexa, what's the weather in")

                # Time and Date
                elif "time" in query:
                    strTime = datetime.datetime.now().strftime("%I:%M %p")

                    show_Siri(f"The current time is {strTime}")


                elif 'date' in query:
                    date = datetime.date.today()
                    show_Siri(str(date))


            except Exception as e:
                show_Siri('Please repeat yourself')

        # =====================================================

        def destroyWindow():
            self.screen.destroy()
            main()

        # =====================================================
        # Initialization

        # ti update Siri animated image
        label = Label(self.screen)
        label.pack()
        self.screen.after(0, update, 0)

        # =====================================================


        self.received_command = tk.Label(self.screen, text='', font=(self.font_), fg='green', justify=CENTER)
        self.received_command.place(x=15, y=330)


        # =====================================================

        # =====================================================
        # App Logic is here

        while True:

            VoiceAssistant()




'''
Main
'''

if __name__ == "__main__":


    engine = pyttsx3.init('sapi5')
    # engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 190)

    WAKE = 'hello'

    main()