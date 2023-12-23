# WENDI

## Introduction
The Wellesley Evaluation Network for Dorm Information (WENDI) is a web tool designed to streamline the housing selection journey. WENDI facilitates effortless navigation through campus housing options, enhanced by genuine peer reviews and data inputs from fellow students. This tool allows users to report and share insights about the rooms they and their peers have lived in, offering a rich source of real-world data and experiences. Students seeking room insights will find a wealth of information, while those wanting to share experiences have a platform to amplify their voices.

## Contributors
- Annabel Yao (yy102@wellesley.edu)
- Emma Lim (el110@wellesley.edu)
- Hae Rin Hong (hhong6@wellesley.edu)
- Veronica Lin (yl102@wellesley.edu)

## Video Demo
- [Click here to download the video demo](./WENDI_finalDemo.mp4)
- [Click here to view the video demo on Google Drive](https://drive.google.com/drive/folders/14-mplFHYxd89QbULS8cfanUY21xxmupp?usp=sharing)

## Technology Stack
- **Flask**: Used as the web framework
- **MySQL**: Database for storing user data and reviews
- **HTML/CSS**: For structuring and styling the web pages

## Main Features

### User Registration/Join Page
- Allows new users to create an account with us
- Hashes passwords with Bcrypt
- Implements sessions so that only logged-in users can post a review/access previous reviews

### Landing Page
- Displays all residential halls, categorized by complex
- Interactive elements to navigate to specific dorms

### Dorm Page
- Lists rooms in the selected dorm
- Room filtering by capacity
- Links to individual room pages

### Room Page
- Shows reviews and comments for a specific room
- Ability to submit comments (requires login)

### Room Review Page
- Form to submit reviews for a specific room
- Options to rate various aspects of the room and attach images

### Home Page
- Personalized space for users to navigate their reviews and comments
- Links to individual review/comment pages

## Endpoints

### `/join/`
- User registration page

### `/login/`
- Login page for existing users

### `/about/`
- Information about the WENDI platform

### `/home/`
- User-specific home page

### `/browse-all/`
- Landing page to see all halls

### `/browse/<complex_type>/`
- Shows dorms in a specific complex

### `/dorm/<dorm_name>`
- Displays rooms in a specified dorm

### `/dorm/<dorm_name>/room/<room_number>`
- Room-specific page with reviews and comments

### `/review/`
- Page for submitting room reviews

