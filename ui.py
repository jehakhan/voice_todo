import tkinter as tk
from db import list_today_tasks, mark_completed
from reminder import run_reminders
from main import main as add_task_voice

root = tk.Tk()
root.title("Voice Todo")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Today's Tasks", font=("Arial", 14)).pack()

task_frame = tk.Frame(frame)
task_frame.pack(pady=10)

def refresh_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()

    tasks = list_today_tasks()
    for task_id, task_text in tasks:
        var = tk.IntVar()
        cb = tk.Checkbutton(
            task_frame,
            text=task_text,
            variable=var,
            command=lambda tid=task_id: mark_completed(tid)
        )
        cb.pack(anchor="w")

refresh_tasks()

tk.Button(frame, text="🎤 Add Task (Voice)", command=add_task_voice).pack(pady=5)
tk.Button(frame, text="🔔 Run Reminders Now", command=lambda: run_reminders(force=True)).pack(pady=5)

root.mainloop()
