import datetime
import random
import pyttsx3
import requests
import openai
from playsound import playsound
from googlesearch import search

engine = pyttsx3.init()
openai.api_key = "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"

def speak(text):
    play_beep()
    engine.say(text)
    engine.runAndWait()
    play_beep()

def play_beep():
    playsound("beep.mp3")  # Add a short beep sound file to your folder

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}"

def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the developer go broke? Because he used up all his cache.",
        "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats."
    ]
    return random.choice(jokes)

def get_weather(city="Pune"):
    api_key = "YOUR_WEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The weather in {city} is {desc} with a temperature of {temp}°C."
    else:
        return f"Couldn't fetch weather for {city}."

def get_news():
    api_key = "YOUR_NEWS_API_KEY"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        headlines = [article["title"] for article in data["articles"][:5]]
        return "Top headlines:\n" + "\n".join(f"- {headline}" for headline in headlines)
    else:
        return "Couldn't fetch news."

def gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {e}"

def web_search(query):
    results = list(search(query, num_results=3))
    return "Here are some results:\n" + "\n".join(results)

def log_interaction(command, response):
    with open("jarvis_log.txt", "a") as file:
        file.write(f"User: {command}\nJarvis: {response}\n\n")

def handle_command(command):
    command = command.lower()
    if "time" in command:
        response = get_time()
    elif "joke" in command:
        response = tell_joke()
    elif "weather" in command:
        response = get_weather()
    elif "news" in command:
        response = get_news()
    elif "chat" in command or "explain" in command:
        response = gpt_response(command)
    else:
        response = web_search(command)
    log_interaction(command, response)
    return response
import speech_recognition as sr
from jarvis_core import handle_command, speak

def listen_loop():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis is listening in background...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                if "jarvis" in command.lower():
                    query = command.replace("jarvis", "").strip()
                    response = handle_command(query)
                    print("Jarvis:", response)
                    speak(response)
            except:
                continue

listen_loop()
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import speech_recognition as sr
from jarvis_core import handle_command, speak

def listen_and_respond():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            status_label.config(text=f"You said: {command}")
            response = handle_command(command)
            output_text.set(response)
            speak(response)
        except sr.UnknownValueError:
            output_text.set("Sorry, I didn't catch that.")
        except sr.RequestError:
            output_text.set("Speech recognition service is down.")
        except Exception as e:
            output_text.set(f"Error: {e}")
        status_label.config(text="Ready")

def run_text_command():
    command = input_entry.get()
    response = handle_command(command)
    output_text.set(response)
    speak(response)

def pulse_avatar():
    global pulse_state
    new_size = 110 if pulse_state else 100
    resized = avatar_img.resize((new_size, new_size))
    avatar_photo_updated = ImageTk.PhotoImage(resized)
    avatar_label.config(image=avatar_photo_updated)
    avatar_label.image = avatar_photo_updated
    pulse_state = not pulse_state
    root.after(500, pulse_avatar)

# GUI setup
root = tk.Tk()
root.title("Jarvis Assistant")
root.geometry("400x400")
root.configure(bg="#1e1e1e")

# Avatar
avatar_img = Image.open("avatar.png").resize((100, 100))
avatar_photo = ImageTk.PhotoImage(avatar_img)
avatar_label = tk.Label(root, image=avatar_photo, bg="#1e1e1e")
avatar_label.pack(pady=5)
pulse_state = False
pulse_avatar()

# Input
input_entry = tk.Entry(root, width=40, bg="#2e2e2e", fg="white", insertbackground="white")
input_entry.pack(pady=10)

run_button = tk.Button(root, text="Run Text Command", command=run_text_command, bg="#3e3e3e", fg="white")
run_button.pack()

voice_button = tk.Button(root, text="🎙️ Speak", command=listen_and_respond, bg="#3e3e3e", fg="white")
voice_button.pack(pady=5)

status_label = tk.Label(root, text="Ready", fg="#00ffcc", bg="#1e1e1e")
status_label.pack()

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, wraplength=350, justify="left", fg="white", bg="#1e1e1e")
output_label.pack(pady=10)

root.mainloop()
import requests

# Optional: Replace with your Puter API key if authentication is required
API_KEY = "YOUR_PUTER_API_KEY"

def puter_ai_chat(prompt, model="gpt-4.1-nano"):
    url = "https://api.puter.com/v2/ai/chat"
    headers = {
        "Content-Type": "application/json",
        # Uncomment the line below if API key is needed
        # "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "prompt": prompt,
        "model": model
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", "No response field found.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage
if __name__ == "__main__":
    prompt = "What are the benefits of exercise?"
    result = puter_ai_chat(prompt)
    print(result)
    from puter import ChatCompletion

response = ChatCompletion.create(
    messages=[{"role": "user", "content": "Tell me a joke"}],
    model="gpt-4o-mini",
    driver="openai-completion",
    api_key="your-api-key"  # Replace with your actual Puter API key
)

print(response)
from flask import Flask, request, jsonify
from jarvis_core import chat_with_gpt, get_weather, get_news, detect_sentiment, set_reminder

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    reply = chat_with_gpt(user_input)
    return jsonify({"reply": reply})

@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "Hyderabad")
    report = get_weather(city)
    return jsonify({"weather": report})

@app.route("/news", methods=["GET"])
def news():
    headlines = get_news()
    return jsonify({"headlines": headlines})

@app.route("/sentiment", methods=["POST"])
def sentiment():
    text = request.json["text"]
    mood = detect_sentiment(text)
    return jsonify({"mood": mood})

@app.route("/reminder", methods=["POST"])
def reminder():
    task = request.json["task"]
    time_str = request.json["time"]
    set_reminder(task, time_str)
    return jsonify({"status": "Reminder set"})

if __name__ == "__main__":
    app.run(debug=True)
    import tkinter as tk
import requests

def launch_gui():
    root = tk.Tk()
    root.title("Jarvis AI")
    root.geometry("600x400")

    chat_log = tk.Text(root, bg="black", fg="white", font=("Courier", 12))
    chat_log.pack(expand=True, fill="both")

    entry = tk.Entry(root, font=("Courier", 12))
    entry.pack(fill="x")

    def send_command():
        user_input = entry.get()
        chat_log.insert(tk.END, f"You: {user_input}\n")
        response = requests.post("http://localhost:5000/chat", json={"message": user_input}).json()["reply"]
        chat_log.insert(tk.END, f"Jarvis: {response}\n")
        entry.delete(0, tk.END)

    entry.bind("<Return>", lambda event: send_command())
    root.mainloop()
    import tkinter as tk
import requests

def launch_gui():
    root = tk.Tk()
    root.title("Jarvis AI")
    root.geometry("600x400")
    root.configure(bg="#1e1e1e")

    chat_log = tk.Text(root, bg="black", fg="white", font=("Courier", 12))
    chat_log.pack(expand=True, fill="both")

    entry = tk.Entry(root, font=("Courier", 12), bg="#2e2e2e", fg="white", insertbackground="white")
    entry.pack(fill="x")

    def send_command():
        user_input = entry.get()
        chat_log.insert(tk.END, f"You: {user_input}\n")
        try:
            response = requests.post("http://localhost:5000/chat", json={"message": user_input})
            reply = response.json().get("reply", "No reply received.")
        except Exception as e:
            reply = f"Error contacting server: {e}"
        chat_log.insert(tk.END, f"Jarvis: {reply}\n")
        entry.delete(0, tk.END)

    entry.bind("<Return>", lambda event: send_command())
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
    import random

def add_personality(response, mood="neutral"):
    styles = {
        "neutral": lambda r: r,
        "friendly": lambda r: f"😊 Sure thing! {r}",
        "sarcastic": lambda r: f"Oh wow, groundbreaking stuff... {r}",
        "excited": lambda r: f"🎉 You got it! {r}",
        "empathetic": lambda r: f"I hear you. {r} Let’s make it better together."
    }
    return styles.get(mood, styles["neutral"])(response)

def detect_mood(text):
    keywords = {
        "sad": ["down", "depressed", "unhappy", "tired"],
        "happy": ["great", "awesome", "excited", "joy"],
        "angry": ["mad", "angry", "furious", "annoyed"],
        "neutral": []
    }
    for mood, words in keywords.items():
        if any(word in text.lower() for word in words):
            return mood
    return "neutral"

def personality_response(command, raw_response):
    mood = detect_mood(command)
    style = "friendly" if mood == "happy" else "empathetic" if mood == "sad" else "neutral"
    return add_personality(raw_response, style)
    return personality_response(command)
import simpleaudio as sa

def play_beep():
    wave_obj = sa.WaveObject.from_wave_file("assets/beep.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
    import vosk
import sounddevice as sd
import queue
import json
from jarvis_core import handle_command, speak
import vosk

model = vosk.Model("vosk-model-small-en-us-0.15")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    q.put(bytes(indata))

def listen_for_wake_word():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("Jarvis is listening in background...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if "jarvis" in text:
                    print("Wake word detected!")
                    speak("Yes, Prasanna?")
                    listen_for_command()

def listen_for_command():
    recognizer = vosk.KaldiRecognizer(model, 16000)
    print("Listening for command...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                command = result.get("text", "")
                if command:
                    print("You said:", command)
                    response = handle_command(command)
                    speak(response)
                    break