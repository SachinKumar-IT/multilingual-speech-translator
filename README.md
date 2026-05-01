# Multilingual Speech‑to‑Speech Translator

A Python application that lets you **speak in your native language** and get **translated text + speech** in any target language.  
Voice commands like **exit** and **change language** work in **any language** – no English required.

## ✨ Features

- 🎤 **Speech recognition** in 20+ languages (including Hindi, Spanish, French, Tamil, etc.)  
- 🔁 **Translation** from source → target language (using Google Translate)  
- 🔊 **Text‑to‑speech** output in the target language  
- 🗣️ **Multilingual voice commands** – say *"salir"* (Spanish), *"बाहर निकलें"* (Hindi), or *"sortir"* (French) to exit or change languages  
- 🌐 Fully offline except for Google Speech & Translate APIs (internet required)  
- 🛡️ Error‑handled (microphone checks, temp files, fallback audio players)

##  How to Use

1. **Clone the repository**  
   ```bash
   git clone https://github.com/SachinKumar-IT/multilingual-speech-translator.git
   cd speech-translator
   
2. **Install dependencies**
 pip install speechrecognition googletrans==4.0.0-rc1 gtts playsound

3. **Run the script**
python translator.py

4.**Follow the prompts**

Select your source language (the language you will speak)
Select your target language (the language you want to translate into)
Speak into the microphone
The translated text will be spoken back in the target language

**Voice commands (speak them in your source language)**
exit → stops the program
change language → resets source/target languages
