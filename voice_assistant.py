"""
Voice Assistant Mini Application
Subject: Text and Speech Analysis
Description: A conversational assistant combining Speech-to-Text (ASR), Natural
             Language Understanding (Intent Classification), Action Fulfillment,
             and Text-to-Speech (TTS). Supports voice and text input modes.
"""

import datetime
import random
import sys
import time

# 1. Text-to-Speech (pyttsx3)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("[WARNING] 'pyttsx3' not installed. Running in silent text-only mode.")

# 2. Speech-to-Text (SpeechRecognition)
try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False
    print("[WARNING] 'SpeechRecognition' not installed. Voice input will be disabled.")

# 3. Wikipedia lookup
try:
    import wikipedia
    WIKI_AVAILABLE = True
except ImportError:
    WIKI_AVAILABLE = False


class MiniVoiceAssistant:
    def __init__(self):
        self.engine = None
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
                self.engine.setProperty("volume", 0.9)
            except Exception as e:
                print(f"[WARNING] Could not initialize TTS engine: {e}")
                self.engine = None

        self.recognizer = sr.Recognizer() if STT_AVAILABLE else None

        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
            "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
            "An acoustic engineer's favorite musical chord is... fundamental frequency!"
        ]

    def speak(self, text):
        """Speaks the response out loud and prints to terminal."""
        print(f"\n[Assistant]: {text}")
        if self.engine is not None:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[TTS Error]: {e}")

    def listen_from_mic(self):
        """Captures voice query from microphone."""
        if not STT_AVAILABLE or self.recognizer is None:
            print("[INFO] SpeechRecognition unavailable. Falling back to text prompt.")
            return input("\n[You (Type)]: ").strip()

        try:
            with sr.Microphone() as source:
                print("\n[Listening] Adjusting for background noise (1s)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("[Listening] Speak your command now (5s timeout)...")
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                except sr.WaitTimeoutError:
                    print("[Mic] No speech detected (Timeout).")
                    return ""

            print("[Processing] Recognizing speech...")
            query = self.recognizer.recognize_google(audio)
            print(f"[You (Voice)]: \"{query}\"")
            return query.lower()

        except (AttributeError, OSError) as e:
            print(f"[Mic Error]: Microphone not accessible ({e}).")
            print("Tip: PyAudio is required for microphone input. Switching to typing.")
            return input("\n[You (Type)]: ").strip()
        except sr.UnknownValueError:
            print("[Mic]: Sorry, I did not catch that.")
            return ""
        except sr.RequestError as e:
            print(f"[Network Error]: Google speech service unreachable: {e}")
            return input("\n[You (Type)]: ").strip()

    def process_command(self, command):
        """NLU Intent Classification and Fulfillment Engine."""
        cmd = command.strip().lower()
        if not cmd:
            return True

        # Intent 1: Exit / Quit
        if any(w in cmd for w in ["exit", "quit", "bye", "goodbye", "stop"]):
            self.speak("Goodbye! Have a productive study session in Text and Speech Analysis.")
            return False

        # Intent 2: Greeting
        elif any(w in cmd for w in ["hello", "hi", "hey", "greetings"]):
            greetings = [
                "Hello! How can I assist you with text and speech analysis today?",
                "Hi there! Ready to assist. What would you like to know?",
                "Greetings! I am your student lab voice assistant."
            ]
            self.speak(random.choice(greetings))

        # Intent 3: Identity / Who are you
        elif "who are you" in cmd or "what is your name" in cmd:
            self.speak("I am your Text and Speech Analysis mini voice assistant, built using Python!")

        # Intent 4: Time
        elif "time" in cmd:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")

        # Intent 5: Date
        elif any(w in cmd for w in ["date", "day is it", "today"]):
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {current_date}.")

        # Intent 6: Joke
        elif "joke" in cmd:
            self.speak(random.choice(self.jokes))

        # Intent 7: Wikipedia Search / Knowledge lookup
        elif any(w in cmd for w in ["who is", "what is", "tell me about", "wikipedia", "search"]):
            topic = cmd
            for prefix in ["who is", "what is", "tell me about", "wikipedia", "search for", "search"]:
                topic = topic.replace(prefix, "")
            topic = topic.strip(" ?.")

            if not topic:
                self.speak("What topic would you like me to look up?")
                return True

            if not WIKI_AVAILABLE:
                self.speak(f"Wikipedia library is not installed. Looking up '{topic}' is not available.")
                return True

            self.speak(f"Searching Wikipedia for {topic}...")
            try:
                summary = wikipedia.summary(topic, sentences=2)
                self.speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                self.speak(f"There are multiple topics for {topic}. Suggestions include: {', '.join(e.options[:3])}")
            except wikipedia.exceptions.PageError:
                self.speak(f"Sorry, I could not find a Wikipedia page matching '{topic}'.")
            except Exception as e:
                self.speak(f"Sorry, could not complete search due to: {e}")

        # Intent 8: Help
        elif "help" in cmd or "what can you do" in cmd:
            help_msg = (
                "You can ask me: 'What time is it?', 'What is today's date?', "
                "'Tell me a joke', 'Who is Alan Turing?', 'What is speech recognition?', "
                "or say 'Exit' to finish."
            )
            self.speak(help_msg)

        # Fallback Intent
        else:
            self.speak("I didn't quite catch that. Say 'help' to see what commands I can understand.")

        return True


def main():
    print("=" * 65)
    print("      INTERACTIVE VOICE ASSISTANT - MINI LAB")
    print("=" * 65)
    print("Combines ASR (Speech-to-Text), Intent Matching, and TTS (Text-to-Speech).")

    assistant = MiniVoiceAssistant()

    print("\nSelect Input Mode:")
    print("1. Voice Mode (Speaks and listens to your Microphone)")
    print("2. Text Mode  (Type queries in console, assistant speaks replies)")
    mode_choice = input("Enter choice (1 or 2, default 2): ").strip()
    voice_mode = (mode_choice == "1")

    assistant.speak("Voice Assistant initialized and ready. How may I help you?")

    running = True
    while running:
        try:
            if voice_mode:
                user_input = assistant.listen_from_mic()
                if not user_input:
                    continue
            else:
                user_input = input("\n[You (Type)]: ").strip()
                if not user_input:
                    continue

            running = assistant.process_command(user_input)

        except KeyboardInterrupt:
            print("\nSession interrupted by user.")
            assistant.speak("Goodbye!")
            break


if __name__ == "__main__":
    main()
