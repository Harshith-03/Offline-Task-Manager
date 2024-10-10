# Task Manager with Email Notifications

This is a Python-based task manager application that allows users to manage tasks with deadlines and automatically sends email reminders when deadlines are approaching or have passed.

## Features

- Add tasks with a title, description, and deadline.
- Remove tasks based on the task title.
- List all ongoing and completed tasks.
- Automatically send email reminders for tasks that are nearing their deadline or have passed.
- GUI built using `customtkinter` for user-friendly interaction.

## Packages Used

1. **customtkinter**
   - Used to create the graphical user interface (GUI) for adding, removing, and listing tasks.
   - Documentation: [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
   
2. **smtplib**
   - The built-in Python library used for sending emails via SMTP (Simple Mail Transfer Protocol).

3. **email.mime.multipart** and **email.mime.text**
   - Used for formatting the email content (subject, body, etc.) in both plain text and HTML.

4. **schedule**
   - Used to schedule the task deadline checking process. It periodically checks if any task deadlines are near or have passed.
   - Documentation: [schedule](https://pypi.org/project/schedule/)

5. **json**
   - Used to save and load tasks from a `tasks.json` file to keep track of task information (title, description, deadline).

6. **tkcalendar**
   - Used to make it easier to select dates for the task deadlines in the GUI.
   - Documentation: [tkcalendar](https://pypi.org/project/tkcalendar/)

7. **datetime**
   - Used for handling the date and time related to task deadlines.

## How to Use

1. **Install the Required Packages**  
   You can install the required Python packages using `pip`. Run the following command in your project folder:
   ```bash
   pip install customtkinter schedule tkcalendar
   ```

   

2. **Run the Application**
Once all packages are installed, you can run the application using:
   ```bash
   python task_manager.py
   ```

   

3. **Using the GUI**

- Add Task: Enter a task title, description, and choose a deadline. Click "Add Task" to save it.
- Remove Task: Enter the task title to remove it and click "Remove Task."
- List Tasks: Click the "List Tasks" button to display all ongoing tasks.
- Start Scheduler: The app automatically starts checking for task deadlines once the GUI is running.

  

4. **Email Notifications**
The application sends automatic email notifications when:

A task's deadline is approaching.
A task's deadline has passed.
You will need to provide your own email credentials in the code (replace the placeholders with your own):
  ```bash
  from_email = "youremail@gmail.com"
  password = "yourpassword"
  ```



5. **Future Enhancements**
- Improved security for storing email credentials.
- Adding authentication for multiple users.
- Hosting the app online for remote access.

  

6. **License**
This project is licensed under the MIT License.
