from voice import listen_once
from nlu import extract_task_and_date
from db import init_db, add_task, list_today_tasks, carry_forward

import pyttsx3
import time

# Speak engine
def speak(text):
    engine = pyttsx3.init()
    time.sleep(0.4)
    print(text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# Initialize database and carry forward incomplete tasks
init_db()
carry_forward()


def listen_confirmation(retries=3):
    for i in range(retries):
        confirm = listen_once()

        if confirm:
            return confirm.lower()
        else:
            speak("I could not understand. Please repeat.")
    return ""  # after max retries



def handle_task_lifecycle():
    """Complete lifecycle for a single trigger: listen -> parse -> confirm -> add/discard"""
    speak("Please say your task")
    command = listen_once()

    if not command:
        speak("No command detected.")
        return

    # Extract task + due date
    task_text, due_date = extract_task_and_date(command)

    print(f"\nTask: {task_text}")
    print(f"Due: {due_date}")

    # Ask for confirmation
    speak(f"Do you want to add task: {task_text} due on {due_date}? Say Yes or No")
    confirmation = listen_confirmation()
    if "yes" in confirmation:
        add_task(task_text, due_date)
        speak("Task added successfully!")
    else:
        speak("Task discarded.")

    # List today's tasks
    today_tasks = list_today_tasks()
    if today_tasks:
        speak("Here are your tasks for today.")
        for t in today_tasks:
            print("-", t[1])
            speak(t[1])
    else:
        # print("\nNo tasks for today.")
        speak("You have no tasks for today.")


def main():
    speak("Hello! Press Enter to add a new task.")
    while True:
        input("\nPress Enter to trigger a new task...")
        handle_task_lifecycle()


if __name__ == "__main__":
    main()
