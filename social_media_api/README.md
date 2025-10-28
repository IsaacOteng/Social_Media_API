# Social Media API

A Django REST API for a social media platform with features like user follows, feeds, likes, and notifications.

## Features

### User Management
- Custom user model with profile information
- User registration and authentication
- Follow/Unfollow functionality

### Posts
- Create, read, update, and delete posts
- Comment on posts
- Like/Unlike posts
- Personalized feed based on followed users

### Notifications
- Receive notifications for:
  - New followers
  - Likes on posts
  - Comments on posts

## API Endpoints

### Authentication
- `POST /accounts/register/` - Register a new user
- `POST /accounts/login/` - Login and get authentication token
- `GET /accounts/profile/` - Get current user's profile

### User Interactions
- `POST /accounts/follow/<user_id>/` - Follow a user
- `POST /accounts/unfollow/<user_id>/` - Unfollow a user

### Posts
- `GET /posts/` - List all posts
- `POST /posts/` - Create a new post
- `GET /posts/<id>/` - Get post details
- `PUT /posts/<id>/` - Update a post
- `DELETE /posts/<id>/` - Delete a post
- `POST /posts/<id>/like/` - Like a post
- `POST /posts/<id>/unlike/` - Unlike a post
- `GET /posts/feed/` - Get personalized feed

### Comments
- `GET /comments/` - List all comments
- `POST /comments/` - Create a new comment
- `GET /comments/<id>/` - Get comment details
- `PUT /comments/<id>/` - Update a comment
- `DELETE /comments/<id>/` - Delete a comment

### Notifications
- `GET /notifications/` - Get user's notifications

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd social_media_api
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Follow a User
```bash
curl -X POST http://localhost:8000/accounts/follow/2/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### Create a Post
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Post","content":"Hello World!"}'
```

### Like a Post
```bash
curl -X POST http://localhost:8000/posts/1/like/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### Get Feed
```bash
curl -X GET http://localhost:8000/posts/feed/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

## Authentication

All endpoints except registration and login require authentication. Include your authentication token in the request headers:

```
Authorization: Token YOUR_AUTH_TOKEN
```

You can obtain a token by logging in with your credentials at `/accounts/login/`.