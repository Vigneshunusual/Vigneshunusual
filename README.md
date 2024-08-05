# overview

This project is a keylogger that captures keystrokes, checks for forbidden keywords, encrypts sensitive data, and sends alerts via email. It is intended for educational purposes and should be used responsibly.

# snapshots

![output](https://github.com/user-attachments/assets/96fd441c-f581-45e3-9277-bf630e44e9f5)

![scrnshot capture](https://github.com/user-attachments/assets/a9072a8b-a80f-4886-be5f-9ba7521acf90)

![EMAIL](https://github.com/user-attachments/assets/d273121d-1325-48d4-bc0c-35b2c8c6d98d)

![generate key output](https://github.com/user-attachments/assets/5b43ff5b-7f27-48a5-82fa-4afca16915a4)

![decryption  pic](https://github.com/user-attachments/assets/610647b3-c4b4-4953-bfe1-2a407a590807)

# Inputs To Mail

Get Keyboard,ScreenShot,Microphone Inputs and Send to your Mail. 


# Features

1.Keystroke Logging: Captures all keystrokes typed by the user.

2.Forbidden Keyword Detection: Checks for a list of predefined forbidden keywords.

3.Data Encryption: Encrypts captured data, including keystrokes, system info, clipboard content, and screenshots.

4.Alarm Triggering: Triggers an alarm sound when forbidden keywords are detected.

5.Microphone Recording: Records audio when forbidden keywords are detected.

6.Email Notifications: Sends email notifications with encrypted attachments when forbidden keywords are detected.

7.System Information Collection: Captures and encrypts system information.

8.Clipboard Monitoring: Captures and encrypts clipboard content.

9.Screenshot Capture: Takes screenshots and saves them without encryption.

# Installation

1.Install Required Packages:

   pip install -r requirements.txt

   Packages: time, winsound, smtplib, email, pyperclip, pyautogui, sounddevice, numpy, scipy, pynput, cryptography, platform, socket, requests, base64

2.Configure Email Settings:

   Update the sender_email, receiver_email, and email_password variables with your email credentials.








