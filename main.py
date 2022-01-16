import sys

from neuralintents.neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts

recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.getProperty('rate')

todo_list = ["Go Shopping", "Clean room", "Record Video"]

def create_note():
    global recognizer

    speaker.say("What do you want to write on to your note!")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                item = note.lower()

                todo_list.append(item)

                done = True
                speaker.say(f"I addded {item} to the to do list!")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again.")


def show_todos():
    speaker.say("The items on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Hello. What can I do for you?")
    speaker.runAndWait()

def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    "greeting": hello,
    "exit": quit,
    "create_note": create_note,
    "show_todos": show_todos,
}


assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message.lower()
        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()