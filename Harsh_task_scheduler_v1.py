# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:12:03 2024

@author: harsh
"""

import json
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import customtkinter as ctk 
from tkinter import messagebox, Listbox
from tkcalendar import DateEntry

# Set up Customtkinter appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Loading tasks from JSON
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Saving tasks to a JSON file
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# Add a new task from the GUI
def add_task_gui():
    title = title_entry.get()
    description = desc_entry.get()
    deadline_date = date_entry.get_date()  
    hour = hour_entry.get()
    minute = minute_entry.get()
    
    try:
        deadline = datetime.combine(deadline_date, datetime.strptime(f"{hour}:{minute}", "%H:%M").time())
        
    except ValueError:
        messagebox.showerror("Invalid time format", "Please enter a valid hour and minute")
        return
     
    tasks = load_tasks()

    task = {
        "title": title,
        "description": description,
        "deadline": deadline.strftime('%Y-%m-%d %H:%M:%S'),
        "reminder_sent": False,
        "completed": False  
    }

    tasks.append(task)
    save_tasks(tasks)
    messagebox.showinfo("Success", "Task added successfully!")
    clear_entries()

    # Start scheduling after task is added
    start_scheduler()

# Remove a task from the GUI
def remove_task_gui():
    title_to_remove = title_entry.get()
    tasks = load_tasks()
    tasks = [task for task in tasks if task['title'] != title_to_remove]
    save_tasks(tasks)
    messagebox.showinfo("Success", "Task removed successfully!")
    clear_entries()

# List all tasks (separating ongoing and completed)
def list_tasks():
    tasks = load_tasks()
    
    if ongoing_listbox.winfo_exists():
        ongoing_listbox.delete(0, ctk.END)

    if completed_listbox.winfo_exists():
        completed_listbox.delete(0, ctk.END)
    
    for task in tasks:
        if task["completed"]:
            completed_listbox.insert(ctk.END, f'{task["title"]} - Completed')
        else:
            ongoing_listbox.insert(ctk.END, f'{task["title"]} - Deadline: {task["deadline"]}')
            

# Email notification function
def send_email(subject, body, to_email):
    from_email = "harsh.taskmanager@gmail.com"
    password = "gtiv jbcg itth hbvi"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Check deadlines and move completed tasks
def check_deadlines():
    tasks = load_tasks()
    now = datetime.now()
    updated_tasks = []

    for task in tasks:
        deadline = datetime.strptime(task['deadline'], '%Y-%m-%d %H:%M:%S')
        time_until_deadline = deadline - now
        
        
        if not task.get("reminder_sent") and time_until_deadline <= timedelta(minutes=30):
            send_email(
                subject="Deadline Approaching",
                body=f"Reminder: The deadline for {task['title']} is in 30 minutes.",
                to_email="harshithrajkumar25@gmail.com"
            )
            task["reminder_sent"] = True

        if deadline <= now and not task.get("completed", False):
            send_email(
                subject="Deadline Passed",
                body=f"Reminder: The deadline for {task['title']} has passed.",
                to_email="harshithrajkumar25@gmail.com"
            )
            task["completed"] = True  # Mark task as completed
        updated_tasks.append(task)

    save_tasks(updated_tasks)
    list_tasks()  # Refresh the list view

# Clear the input fields
def clear_entries():
    title_entry.delete(0, ctk.END)
    desc_entry.delete(0, ctk.END)
    hour_entry.delete(0, ctk.END)
    minute_entry.delete(0, ctk.END)
    

# Scheduler start function
def start_scheduler():
    schedule.every(1).minutes.do(check_deadlines)
    run_scheduler()

    # Run the scheduler in a separate thread to avoid blocking the GUI
def run_scheduler():
    schedule.run_pending()
    app.after(1000, run_scheduler)
            

# GUI SETUP
app = ctk.CTk()
app.title("Task Manager")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.geometry(f"{screen_width}x{screen_height}+0+0")

# Set a theme (adjust based on preferences)
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")  

# Font settings
font_large = ("Helvetica", 18, "bold")
font_medium = ("Helvetica", 14)
font_small = ("Helvetica", 12)

# Layout colors and style
bg_color = "#f0f0f0"  
button_color = "#333333"  
text_color = "#ffffff"  
box_bg_color = "#d9d9d9"  

app.configure(bg=bg_color)

# Create a frame for the main layout to spread content evenly
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Configure grid layout to evenly spread content
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

# Task Scheduling Section (Left Column)
frame_left = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=bg_color)
frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

title_label = ctk.CTkLabel(frame_left, text="SCHEDULE TASKS", font=font_large, bg_color=bg_color)
title_label.pack(pady=10)

# Labels and Entries for Task Inputs
ctk.CTkLabel(frame_left, text="TASK TITLE:", font=font_medium).pack(anchor='w', padx=10)
title_entry = ctk.CTkEntry(frame_left, width=250)
title_entry.pack(pady=5)

ctk.CTkLabel(frame_left, text="TASK DESCRIPTION:", font=font_medium).pack(anchor='w', padx=10)
desc_entry = ctk.CTkEntry(frame_left, width=250)
desc_entry.pack(pady=5)

# Date Picker for Deadline
ctk.CTkLabel(frame_left, text="DEADLINE DATE:", font=font_medium).pack(anchor='w', padx=10)
date_entry = DateEntry(frame_left, width=30, date_pattern='y-mm-dd')  # tkcalendar DateEntry for picking the date
date_entry.pack(pady=5)

# Separate fields for Hours and Minutes
ctk.CTkLabel(frame_left, text="DEADLINE TIME (HH:MM):", font=font_medium).pack(anchor='w', padx=10)
time_frame = ctk.CTkFrame(frame_left, fg_color=bg_color)
time_frame.pack(pady=5)

hour_entry = ctk.CTkEntry(time_frame, width=50)
hour_entry.pack(side="left", padx=5)
ctk.CTkLabel(time_frame, text=":", font=font_medium).pack(side="left")
minute_entry = ctk.CTkEntry(time_frame, width=50)
minute_entry.pack(side="left", padx=5)

# Buttons for Task Actions
add_button = ctk.CTkButton(frame_left, text="ADD TASK", command=add_task_gui, fg_color=button_color, text_color=text_color)
add_button.pack(pady=10)

delete_button = ctk.CTkButton(frame_left, text="DELETE TASK", command=remove_task_gui, fg_color=button_color, text_color=text_color)
delete_button.pack(pady=5)

# Ongoing Tasks Section (Center Column)
frame_center = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=bg_color)
frame_center.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

ongoing_label = ctk.CTkLabel(frame_center, text="ONGOING TASKS", font=font_large, bg_color=bg_color)
ongoing_label.pack(pady=10)

# Listbox for ongoing tasks
ongoing_listbox = Listbox(frame_center, width=50, height=25, bg=box_bg_color, font=font_small, relief="flat")
ongoing_listbox.pack(pady=5)

# Completed Tasks Section (Right Column)
frame_right = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=bg_color)
frame_right.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

completed_label = ctk.CTkLabel(frame_right, text="COMPLETED TASKS", font=font_large, bg_color=bg_color)
completed_label.pack(pady=10)

# Listbox for completed tasks
completed_listbox = Listbox(frame_right, width=50, height=25, bg=box_bg_color, font=font_small, relief="flat")
completed_listbox.pack(pady=5)

# Start the main loop
app.mainloop()


