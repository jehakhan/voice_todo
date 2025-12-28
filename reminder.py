from db import get_today_pending_tasks, mark_completed, mark_reminded
from voice import listen_once
import pyttsx3
import time


def speak(text):
    engine = pyttsx3.init()
    time.sleep(0.2)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def run_reminders(force):
    tasks = get_today_pending_tasks(force)

    if not tasks:
        speak("You have no pending tasks for today.")
        return

    speak(f"You have {len(tasks)} tasks today.")

    for task_id, task_text in tasks:
        speak(f"Task: {task_text}. Did you complete this task?")

        response = listen_once()

        if response and any(x in response for x in ["yes", "done", "completed"]):
            mark_completed(task_id)
            speak("Marked as completed.")
        else:
            speak("Okay, I will remind you later.")

        mark_reminded(task_id)


# if __name__ == "__main__":
#     run_reminders()
import argparse
from db import get_today_pending_tasks

parser = argparse.ArgumentParser()
parser.add_argument("--force", action="store_true", help="Force repeat reminders")
args = parser.parse_args()
print(args.force)
tasks = run_reminders(force=args.force)
