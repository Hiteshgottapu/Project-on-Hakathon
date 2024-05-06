import threading
import requests
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

# Initialize recognizer and microphone
r = sr.Recognizer()
stop_listening = False

class TranslatorApp(App):
    def build(self):
        self.passenger_language = TextInput(hint_text="Passenger's Language (e.g., 'en' for English)")
        self.employee_language = TextInput(hint_text="Employee's Language (e.g., 'en' for English)")
        self.status_label = Label(text="Status: Waiting for input...")
        self.switch_button = Button(text="Start Translation")
        self.stop_button = Button(text="Stop Listening", state="normal")  # Set initial state to 'normal'

        self.switch_button.bind(on_release=self.start_translation_thread)
        self.stop_button.bind(on_release=self.stop_listening_thread)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.passenger_language)
        layout.add_widget(self.employee_language)
        layout.add_widget(self.status_label)
        layout.add_widget(self.switch_button)
        layout.add_widget(self.stop_button)

        return layout

    def recognize_speech(self, language):
        global stop_listening
        with sr.Microphone() as source:
            # Adjust for ambient noise to reduce background noise
            r.adjust_for_ambient_noise(source, duration=1)
            self.status_label.text = f"Please speak something in {language}..."
            audio = r.listen(source)

            if stop_listening:
                return None

        try:
            # Recognize speech using the specified input language
            user_speech = r.recognize_google(audio, language=language)
            self.status_label.text = f"You said ({language}): {user_speech}"
            return user_speech

        except sr.UnknownValueError:
            self.status_label.text = "Could not understand audio"
            return None

    def translate_text(self, text, source_language, target_language):
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_language,
            "tl": target_language,
            "dt": "t",
            "q": text,
        }

        response = requests.get(base_url, params=params)
        translation = response.json()[0][0][0]
        return translation

    def speak_text(self, text, language):
        tts = gTTS(text=text, lang=language)
        tts.save("output.mp3")  # Save the speech to a file
        playsound.playsound("output.mp3")  # Play the saved speech
        # Remove the temporary file
        os.remove("output.mp3")

    def translate_and_speak(self):
        global stop_listening
        current_language = self.passenger_language.text
        self.switch_button.state = "disabled"
        self.stop_button.disabled = False  # Set 'disabled' property to True

        while True:
            if current_language == self.passenger_language.text:
                self.status_label.text = "Switched to Passenger's language."
            else:
                self.status_label.text = "Switched to Employee's language."

            user_speech = self.recognize_speech(current_language)

            if user_speech:
                target_language = self.employee_language.text if current_language == self.passenger_language.text else self.passenger_language.text
                translated_text = self.translate_text(user_speech, current_language, target_language)
                self.status_label.text = f"Translated text: {translated_text}"
                self.speak_text(translated_text, target_language)

            current_language = self.passenger_language.text if current_language == self.employee_language.text else self.employee_language.text

    def start_translation_thread(self, instance):
        global stop_listening
        stop_listening = False
        translation_thread = threading.Thread(target=self.translate_and_speak)
        translation_thread.daemon = True
        translation_thread.start()
        self.switch_button.state = "disabled"
        self.stop_button.disabled = False

    def stop_listening_thread(self, instance):
        global stop_listening
        stop_listening = True
        self.switch_button.state = "normal"
        self.stop_button.disabled = True  # Set 'disabled' property to True

if __name__ == "__main__":
    TranslatorApp().run()
