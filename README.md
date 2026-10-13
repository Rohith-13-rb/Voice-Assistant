# 09 - Interactive Voice Assistant Application

## Overview
This application is part of the **Text and Speech Analysis** college lab curriculum. It demonstrates a complete end-to-end **Conversational Voice Agent Pipeline**, connecting:

1. **ASR (Automated Speech Recognition)**: Captures acoustic voice pressure waves from the microphone and transcribes them into text using Google Speech Recognition.
2. **NLU & Intent Dispatcher**: Parses incoming text strings into user intents (Time, Date, Wikipedia Fact, Joke, Help, Exit) with slot extraction.
3. **Action Execution**: Gathers information or queries knowledge bases (e.g. Wikipedia API).
4. **TTS (Text-to-Speech Synthesis)**: Converts the generated response string back into audible speech via `pyttsx3`.

```
[User Speech] ──▶ (Microphone) ──▶ [ASR: SpeechRecognition]
                                            │
                                            ▼ (Text)
[Audible Reply] ◀── (Speaker) ◀─── [TTS: pyttsx3] ◀── [Intent Dispatcher & Wikipedia]
```

---

## Features
- **Dual Input Modes**:
  - **Voice Mode**: Speak into your microphone and hear responses.
  - **Text Console Mode**: Type queries in the terminal and hear the assistant speak answers out loud (ideal when a microphone is not connected or in quiet college libraries).
- **Graceful Fallback**: If PyAudio is not installed or microphone hardware is busy, it smoothly switches to keyboard input without terminating.
- **Built-in Intents**:
  - `Time`: Tells current local time.
  - `Date`: Tells current day and date.
  - `Wikipedia Search`: "Who is Alan Turing?", "What is machine learning?", "Search Python".
  - `Jokes`: Programming and science riddles.
  - `Help`: Summarizes supported voice commands.
  - `Exit / Bye`: Terminates the conversational session.

---

## Prerequisites & Installation

1. Navigate to this folder:
   ```bash
   cd 09_Voice_Assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

> **Note regarding PyAudio on Windows:**
> If you plan to use **Voice Mode** (microphone), `pyaudio` is required. On Windows:
> ```bash
> pip install pyaudio
> ```
> If `pip install pyaudio` fails on your system, simply choose **Mode 2 (Text Mode)** to test the assistant immediately!

---

## How to Run

```bash
python voice_assistant.py
```

### Example Usage (Text Mode):
```text
Select Input Mode:
1. Voice Mode (Speaks and listens to your Microphone)
2. Text Mode  (Type queries in console, assistant speaks replies)
Enter choice (1 or 2, default 2): 2

[Assistant]: Voice Assistant initialized and ready. How may I help you?

[You (Type)]: what time is it
[Assistant]: The current time is 06:40 PM.

[You (Type)]: who is ada lovelace
[Assistant]: Searching Wikipedia for ada lovelace...
[Assistant]: Augusta Ada King, Countess of Lovelace was an English mathematician and writer, chiefly known for her work on Charles Babbage's mechanical general-purpose computer, the Analytical Engine. She was the first to recognize that the machine had applications beyond pure calculation.

[You (Type)]: tell me a joke
[Assistant]: Why do programmers prefer dark mode? Because light attracts bugs!

[You (Type)]: bye
[Assistant]: Goodbye! Have a productive study session in Text and Speech Analysis.
```

---

## Technical Notes & Limitations
- **Internet Requirement**: Online connectivity is required for Wikipedia queries and Google ASR voice recognition.
- **Microphone Permissions**: Windows privacy settings must permit microphone access for Python apps if using Voice Mode.
