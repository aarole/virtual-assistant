from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import os
import playsound
import random
import speech_recognition as sr
from gtts import gTTS

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def speak(text):
	tts = gTTS(text=text, lang="en")
	filename = "voice" + str(random.randint(1, 1000)) + ".mp3"
	#filename = "voice.mp3"
	tts.save(filename)
	playsound.playsound(filename)


def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
			print("you said: " + said)
		except Exception as e:
			print("Exception: " + str(e))
	return said

def auth():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(n, service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event['summary'])
        print(event['start'].get('dateTime', event['start'].get('time')))
    return events


def get_choice():
    speak("Here's a list of things i can do")
    for task in tasks:
        speak(task)
    speak("what option would you like to choose")


def after_choice(choice):
    if "1" or "one" in choice:
        service = auth()
        events = get_events(1, service)
        for event in events:
            speak("you have " + event['summary'] + " at " + event['start'].get('dateTime', event['start'].get('time')))
        speak("is that all you need")
        
    elif "2" or "two" in choice:
        speak("How many events would you like to know")
        num = get_audio()
        service = auth()
        events = get_events(num, service)
        for event in events:
            speak(event['summary'])
        speak("is that all you need")
    elif "3" or "three" in choice:
        get_choice()
        choice_new = get_audio()
        after_choice(choice_new)


speak("Hello, my name is edith. whats your name")

name = get_audio()

speak("Nice to meet you " + name)

get_choice()

choice = get_audio()

after_choice(choice)
