
# AFEX recruitment coding test
## Overview:
### This assessment test is an app built using python and django where user can sign up, sign in, search for other users, can update their profile by uploading a profile picture and a bio, can add friends by sending a friend request, the user or other users on a different browser can view list of friend requests sent by other users, he or she can accept to become friends or reject the request, users who are friends can then chat each other in real time on diffent browsers.
### Note the frontend is minimal which made use of bootstrap as the focus for the test is on the backend.

# Get started

### Creating a virtual environment (for gitbash users)

- run: python -m venv env (To create a virtual environment=> env is the name of your virtual environment in this case)
- run: source env/scripts/activate (To activate the virtual environment)

### Installing Django

- run: pip install django

### Clone the Repository on github

### Project requirements installation:

- pip install -r requirement.txt

### Running the server

- run: python manage.py makemigrations

- run: python manage.py migrate

- python manage.py runserver

### On a different terminal also run the below command and make sure you have docker installed on your local machine:
- docker run -p 6379:6379 -d redis:5
