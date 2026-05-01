import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os
import tempfile
import time
import sys

# Language menu (code : name)
LANGUAGES = {
    '1': ('en', 'English'),
    '2': ('hi', 'Hindi'),
    '3': ('es', 'Spanish'),
    '4': ('fr', 'French'),
    '5': ('de', 'German'),
    '6': ('it', 'Italian'),
    '7': ('ja', 'Japanese'),
    '8': ('ko', 'Korean'),
    '9': ('zh-cn', 'Chinese (Simplified)'),
    '10': ('ar', 'Arabic'),
    '11': ('ru', 'Russian'),
    '12': ('pt', 'Portuguese'),
    '13': ('tr', 'Turkish'),
    '14': ('nl', 'Dutch'),
    '15': ('el', 'Greek'),
    '16': ('he', 'Hebrew'),
    '17': ('ta', 'Tamil'),
    '18': ('te', 'Telugu'),
    '19': ('bn', 'Bengali'),
    '20': ('mr', 'Marathi'),
    '21': ('pa', 'Punjabi'),
    '22': ('gu', 'Gujarati')
}

def choose_language(prompt):
    """Display language menu and return (lang_code, lang_name)."""
    print(f"\n===== {prompt} =====")
    for key, (code, name) in LANGUAGES.items():
        print(f"{key}. {name} ({code})")
    print("================================")
    while True:
        choice = input("Enter the number: ").strip()
        if choice in LANGUAGES:
            return LANGUAGES[choice]
        else:
            print("Invalid choice. Please select a valid number.")

def safe_play_audio(file_path):
    """Play audio with a fallback if playsound fails."""
    try:
        playsound(file_path)
    except Exception as e:
        print(f"Warning: playsound failed ({e}). Trying alternative...")
        if os.name == 'nt':
            os.system(f"start {file_path}")
        elif sys.platform == 'darwin':
            os.system(f"afplay {file_path}")
        elif os.name == 'posix':
            os.system(f"mpg123 {file_path} 2>/dev/null")
        time.sleep(1)

def main():
    # Check microphone availability
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            pass
    except OSError:
        print("ERROR: No microphone found. Please connect a microphone and try again.")
        return
    
    translator = Translator()
    
    print("🎤 Multi‑language Speech-to-Speech Translator")
    print("You can speak in your native language and get translation in another language.")
    print("Commands: say the word for 'exit' or 'change languages' in your native language.\n")
    
    # Select source and target languages
    src_code, src_name = choose_language("Select YOUR language (the language you will speak)")
    tgt_code, tgt_name = choose_language("Select TARGET language (the language you want to translate into)")
    
    print(f"\n✅ Source language: {src_name} ({src_code})")
    print(f"✅ Target language: {tgt_name} ({tgt_code})")
    print("\nSpeak now...\n")
    
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.\n")
                continue
            
            try:
                # Recognize speech in the source language
                speech_text = r.recognize_google(audio, language=src_code)
                speech_text = speech_text.strip()
                if not speech_text:
                    print("Empty speech detected.\n")
                    continue
                
                print(f"You said ({src_name}): {speech_text}")
                
                # ---- COMMAND DETECTION (multilingual) ----
                # Translate the recognized speech to English to check for commands
                try:
                    cmd_translation = translator.translate(speech_text, src=src_code, dest='en').text.lower()
                except Exception:
                    cmd_translation = ""  # fallback, treat as normal speech
                
                if "exit" in cmd_translation or "quit" in cmd_translation:
                    print("Goodbye!")
                    break
                elif "change language" in cmd_translation or "switch language" in cmd_translation:
                    print("Changing languages...")
                    src_code, src_name = choose_language("Select YOUR language (the language you will speak)")
                    tgt_code, tgt_name = choose_language("Select TARGET language (the language you want to translate into)")
                    print(f"\n✅ Source language: {src_name} ({src_code})")
                    print(f"✅ Target language: {tgt_name} ({tgt_code})\n")
                    continue
                
                # ---- NORMAL TRANSLATION ----
                translated = translator.translate(speech_text, src=src_code, dest=tgt_code)
                translated_text = translated.text
                if not translated_text:
                    print("Translation returned empty text.\n")
                    continue
                
                print(f"Translated ({tgt_name}): {translated_text}")
                
                # Text-to-speech in target language
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    voice_file = tmp.name
                tts = gTTS(translated_text, lang=tgt_code)
                tts.save(voice_file)
                safe_play_audio(voice_file)
                os.remove(voice_file)
                print()
                
            except sr.UnknownValueError:
                print(f"Could not understand. Make sure you're speaking {src_name} clearly.\n")
                continue
            except sr.RequestError:
                print("Network error: Cannot reach Google Speech Recognition.\n")
                continue
            except Exception as e:
                print(f"Error: {e}\n")
                continue

if __name__ == "__main__":
    main()