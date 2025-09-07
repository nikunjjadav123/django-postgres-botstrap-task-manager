 Django PostgreSQL Bootstrap Task Manager ( Basic Project )

A simple **Task Manager** web application built with **Django**, **PostgreSQL**, and **Bootstrap 5**.  
Users can add, update, and manage tasks with a clean and responsive interface.

- Add, edit, and delete tasks  
- Mark tasks as completed or pending  
- Task listing with **Bootstrap tables** or **cards**
- Secure configuration with `.env` file
- Login / Change Password / Edit Profile
- Login With JWT Token which access token will expire within 1 min and refresh token will activate upto 7 days

## Tech Stack

- **Backend:** Django 5.2.5
- **Database:** PostgreSQL  
- **Frontend:** Bootstrap 5  25.2
- **Environment Management:** python-decouple  3.8
- **Python Version:** 3.13.5
- **Django Crispy Forms:** 2.4
- **Streamlit:** 1.49.1
## Project Structure

- taskmanager_project/   ← main project folder
- │── manage.py
- │── taskmanager/       ← project config (settings, urls, wsgi, asgi)
- │── accounts/
- │── profiles/
- │── tasks/
- │── templates/
- │── static/
- │── db.sqlite3
