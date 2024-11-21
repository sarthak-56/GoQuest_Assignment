# YouTube Data Fetcher

A Python script that fetches and processes data from a YouTube channel, including details about videos, comments, and replies. The extracted data is saved into an Excel file for easy analysis and reporting.

## Features

- Fetch YouTube channel details using the channel handle.
- Retrieve all videos from a channel with details such as:
  - Title
  - Description
  - Published date
  - View count
  - Like count
  - Comment count
  - Video duration
  - Thumbnail URL
- Fetch all comments and replies for each video.
- Save video and comment data into separate sheets in an Excel file.

## 1.Clone this repository
   git clone https://github.com/sarthak-56/GoQuest_Assignment.git
   
## 2.Create Virtual environment(if virtual environment not activate create a new virtual environment)
   python -m venv env
   
## 3.Activate Virtual environment
   .\env\Scripts\activate
   
## 4.Install all Dependencies
   pip install -r requirements.txt
   
## 5.Run the server
   python manage.py runserver 
