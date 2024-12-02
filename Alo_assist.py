# Import necessary libraries
import tkinter as tk  # For creating the graphical user interface (GUI)
from tkinter import messagebox  # For displaying messages in pop-up dialogs
import speech_recognition as sr  # For voice recognition and listening to user commands
import pyttsx3  # For text-to-speech functionality
import webbrowser  # For opening URLs in the web browser
import random  # For generating random choices (used in jokes and advice)
import requests  # For making HTTP requests to fetch weather data
from youtubesearchpython import VideosSearch  # For searching YouTube videos
import pyjokes  # For generating random jokes
from datetime import datetime  # For fetching and displaying the current date and time

# Initialize the text-to-speech engine
engine = pyttsx3.init()  # Initialize the pyttsx3 engine
voices = engine.getProperty('voices')  # Get the available voices in the system

# Set an Australian female voice for the assistant
for voice in voices:
    if "australian" in voice.name.lower() and "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)  # Set the voice
        break

# Set the speech rate (speed of speech)
engine.setProperty('rate', 180)

# Function to make the assistant speak text
def speak(text):
    """Speak the given text aloud using the text-to-speech engine."""
    print(f"Assistant: {text}")  # Print the assistant's response in the console for debugging
    engine.say(text)  # Convert the text to speech
    engine.runAndWait()  # Wait for the speech to finish

# Function to listen for a voice command from the user
def listen():
    """Listen for a voice command using the microphone and return it as text."""
    recognizer = sr.Recognizer()  # Create a recognizer instance
    with sr.Microphone() as source:  # Use the microphone as the audio source
        try:
            recognizer.dynamic_energy_threshold = True  # Automatically adjust for ambient noise
            recognizer.energy_threshold = 300  # Set the energy threshold for detecting speech
            speak("Listening...")  # Inform the user that the assistant is listening
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Listen for speech input
            command = recognizer.recognize_google(audio, language="en-US")  # Use Google’s speech-to-text API to convert audio to text
            print(f"You: {command}")  # Print the user's command for debugging
            return command.lower()  # Return the recognized command in lowercase
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you repeat?")  # If speech was not understood
            return listen()  # Retry listening if no command was recognized
        except sr.RequestError:
            speak("Oops, I'm having trouble understanding you right now.")  # Handle request errors (API failure)
            return ""  # Return empty string if there was an issue

# Core features of the assistant
def play_song(song_name):
    """Search and play a song on YouTube based on the song name."""
    try:
        videos_search = VideosSearch(song_name, limit=1)  # Search for the song on YouTube
        results = videos_search.result()  # Get the search results
        if results['result']:  # If there is at least one result
            video_url = results['result'][0]['link']  # Get the link to the first video
            webbrowser.open(video_url)  # Open the video in the web browser
            speak(f"Playing {song_name}. Enjoy!")  # Speak to the user
        else:
            speak("Couldn't find that song. Want to try another?")  # If no results were found
    except Exception as e:
        speak("Oops, something went wrong while searching for the song.")  # Handle errors
        print(e)  # Print error to console for debugging

def tell_joke():
    """Tell a random joke using the pyjokes library."""
    joke = pyjokes.get_joke()  # Get a random joke from pyjokes
    speak(joke)  # Speak the joke to the user

def laughs():
    """Respond with a sarcastic laugh when asked."""
    laugh = ["Haha, oh you're so funny.", "I'm dying, really. So hilarious!", "You're on a roll today!", "Oh stop, you're too much."]
    speak(random.choice(laugh))  # Choose a random sarcastic laugh and speak it

def interpret_dream():
    """Redirect to a dream interpretation website."""
    webbrowser.open("https://www.dreammoods.com/")  # Open the dream interpretation site in the browser
    speak("Here's a site to interpret your dreams. Sweet dreams!")  # Speak the response

def tell_date_and_time():
    """Tell the current date and time."""
    now = datetime.now()  # Get the current date and time
    date_time = now.strftime("%A, %B %d, %Y %I:%M %p")  # Format the date and time
    speak(f"Today is {date_time}.")  # Speak the formatted date and time
    return date_time  # Return the formatted date and time string

def get_weather():
    """Fetch and tell the current weather for Rhode Island using OpenWeatherMap API."""
    api_key = "Your API-KEY"  # Replace with your OpenWeatherMap API key  
    city = "Rhode Island, US"  # City for which we want the weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"  # API URL to fetch weather data

    try:
        response = requests.get(url)  # Send a GET request to the weather API
        weather_data = response.json()  # Parse the JSON response

        if weather_data["cod"] == 200:  # If the request was successful
            main = weather_data["weather"][0]["description"].capitalize()  # Get the weather description (e.g., 'clear sky')
            temp = weather_data["main"]["temp"]  # Get the current temperature
            feels_like = weather_data["main"]["feels_like"]  # Get the "feels like" temperature
            speak(f"The weather in Rhode Island is currently {main} with a temperature of {temp}°F. It feels like {feels_like}°F.")  # Speak the weather details
            return f"The weather in Rhode Island is {main} with {temp}°F (feels like {feels_like}°F)."  # Return the weather details as text
        else:
            speak("Sorry, I couldn't fetch the weather right now.")  # If the API response indicates an error
            return "Weather information unavailable."  # Return a fallback message
    except Exception as e:
        speak("Oops, something went wrong while fetching the weather.")  # Handle errors while fetching weather data
        print(e)  # Print error to console for debugging
        return "Error fetching weather."  # Return a fallback message

def give_advice():
    """Provide a random piece of positive advice."""
    advices = [  # List of motivational advice quotes
        "Believe in yourself, you are capable of amazing things.",
        "Don't be afraid to fail. Be afraid not to try.",
        "Stay positive, work hard, and make it happen.",
        "The best way to predict the future is to create it.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Every day is a new opportunity to grow and improve.",
        "Believe you can and you're halfway there.",
        "The only limit to our realization of tomorrow is our doubts of today."
    ]
    advice = random.choice(advices)  # Choose a random piece of advice
    speak(advice)  # Speak the advice to the user

# GUI setup with gradient background
class VirtualAssistantGUI:
    def __init__(self, master):
        self.master = master  # Reference to the main window (Tkinter root)
        master.title("Virtual Assistant")  # Set the window title
        master.geometry("700x500")  # Set the window size

        # Create gradient background for the GUI
        self.canvas = tk.Canvas(master, width=700, height=500)  # Create a canvas widget
        self.canvas.pack(fill="both", expand=True)  # Pack the canvas into the window
        self.create_gradient(self.canvas, "#D8BFD8", "#FFB6C1")  # Call the gradient creation method

        # Add a label asking the user to input a query
        self.label = tk.Label(master, text="Ask me something:", font=("Helvetica", 18, "bold"), bg="#D8BFD8")
        self.label.place(x=50, y=30)  # Position the label in the window

        # Add an input box for the user to type their query
        self.input_box = tk.Entry(master, width=50, font=("Helvetica", 14))
        self.input_box.place(x=50, y=80)  # Position the input box

        # Add a button for the user to ask a query
        self.ask_button = tk.Button(master, text="Ask", command=self.handle_input, font=("Helvetica", 12), bg="#9370DB", fg="white")
        self.ask_button.place(x=50, y=130)  # Position the button

        # Add a button for the user to give a voice command
        self.voice_button = tk.Button(master, text="Voice Command", command=self.voice_command, font=("Helvetica", 12), bg="#9370DB", fg="white")
        self.voice_button.place(x=120, y=130)  # Position the button

        # Add a button to quit the application
        self.quit_button = tk.Button(master, text="Quit", command=master.quit, font=("Helvetica", 12), bg="#8B0000", fg="white")
        self.quit_button.place(x=280, y=130)  # Position the button

        # Add a label to display the assistant's response
        self.response_label = tk.Label(master, text="", font=("Helvetica", 14), wraplength=600, justify="left", bg="#D8BFD8")
        self.response_label.place(x=50, y=200)  # Position the label

    def create_gradient(self, canvas, color1, color2):
        """Create a gradient background on the canvas."""
        width = 700  # Width of the canvas
        height = 500  # Height of the canvas
        gradient_steps = 100  # Number of steps for the gradient effect
        for i in range(gradient_steps):
            ratio = i / gradient_steps  # Calculate the ratio for the gradient transition
            # Calculate the RGB values for the current gradient step
            red = int((1 - ratio) * int(color1[1:3], 16) + ratio * int(color2[1:3], 16))
            green = int((1 - ratio) * int(color1[3:5], 16) + ratio * int(color2[3:5], 16))
            blue = int((1 - ratio) * int(color1[5:7], 16) + ratio * int(color2[5:7], 16))
            color = f"#{red:02x}{green:02x}{blue:02x}"  # Convert RGB to hex
            canvas.create_rectangle(0, i * (height / gradient_steps), width, (i + 1) * (height / gradient_steps), fill=color, outline="")  # Draw the gradient

    def handle_input(self):
        query = self.input_box.get().lower()  # Get the user input from the input box and convert it to lowercase
        self.process_query(query)  # Process the query

    def voice_command(self):
        query = listen()  # Listen for a voice command from the user
        self.process_query(query)  # Process the query

    def process_query(self, query):    
        """Process the user's query and call the appropriate function."""
        if "play a song" in query:
            speak("What song would you like to hear?")  # Ask for the song name
            song_name = listen() or self.input_box.get()  # Get the song name from the user
            play_song(song_name)  # Play the song
        elif "tell me a joke" in query:
            tell_joke()  # Tell a random joke
            speak("Did you like the joke?")  # Ask if the user liked the joke
        elif "laugh at my joke" in query:
            laughs()  # Respond with a sarcastic laugh
        elif "interpret my dream" in query:
            interpret_dream()  # Redirect to the dream interpretation website
        elif "date" in query or "time" in query:
            date_time = tell_date_and_time()  # Get and display the current date and time
            self.response_label.config(text=f"The current date and time is:\n{date_time}")
        elif "weather" in query:
            weather_info = get_weather()  # Fetch and display the weather
            self.response_label.config(text=weather_info)
        elif "what is your name" in query or "who are you" in query:
            speak("Good day mate! My name is Aelo. How are you doing today?")  # Introduce the assistant
            self.response_label.config(text="Good day mate! My name is Aelo. How are you doing today?")
        elif "what do you like to do" in query or "what are your hobbies" in query:
            response = "Well, I'm an Aussie who loves to wrestle with animals, take a dip in the ocean and cook on the barbie. Virtually, of course!"  # Assistant’s hobbies
            speak(response)  # Speak the response
            self.response_label.config(text=response)  # Display it in the GUI
        elif "give me advice" in query:
            give_advice()  # Provide a random piece of advice
        elif "goodbye aelo" in query:
            speak("Goodbye! Have a great day!")  # Say goodbye and quit the app
            self.master.quit()  # Close the GUI and exit the program
        else:
            self.response_label.config(text="I didn't get that. Try again!")  # Handle unrecognized queries
            speak("I didn't quite understand that. Care to rephrase?")  # Ask the user to try again

# Main function to run the program
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    gui = VirtualAssistantGUI(root)  # Create an instance of the VirtualAssistantGUI class
    speak("hello mate! Your virtual assistant here, is ready to roll.")  # Greet the user
    root.mainloop()  # Start the Tkinter event loop to display the GUI
