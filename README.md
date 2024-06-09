 
# Django Application

## Table of Contents
- user (user personal informations)
- friends (user's friend requests)

## Introduction
This is a Django application for a social networking site. It includes user authentication, profile management, and a friends system. The project have Postman collection for API testing.

## Features
- User authentication (login, signup)
- Search users by email or name
- Send, accept, and reject friend requests
- List friends
- List pending friend requests
- Limit on sending friend requests (maximum 3 requests per minute)

## Installation

### Local Development
Follow these steps to set up the project for local development.

#### Prerequisites
- Python 3.8+
- pip
- virtualenv
- any database of your choice


#### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd social_networking

2. **create virtualenv**
    create virtual environment using this command: 
    - python -m venv env
    active the env :
    - cd env\Scripts\activate


3. **create log folder**
    create folder log folder from social_networking 
    - mkdir log

4. **Install packages from requirements.txt**
    pip install requirements.txt

5. **create .env file**
    create .env file for Database informations ans secret keys:
    - export ENGINE= 
    - export NAME= 
    - export USER= 
    - export PASSWORD = 
    - export HOST= 
    - export PORT = 

6. **make python migrations**
    create database named as .env file
    python manage.py makemigrations
    python manage.py migrate

7. **Run server**
    python manage.py runserver

8. **Import postman collections from social_networking postman_collection**
    Import postman_collection JSON file in postman website or app


