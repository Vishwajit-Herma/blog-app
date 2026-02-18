
# Blog Application

A Django-based blogging platform with user authentication, blog management, and commenting features.

## Features

- **User Authentication**: Login required for all features
- **Blog Management**: Create, read, update, and delete blogs
- **Comments**: Add comments to blogs
- **Likes**: Like blogs and comments
- **View Tracking**: Track blog views using sessions
- **Search**: Search blogs by title, content, or author
- **Pagination**: Browse blogs with pagination support

## Installation

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

## Usage

- Create an account and log in
- Create, edit, or delete your blogs
- Comment on other blogs
- Like blogs and comments
- Search for blogs

## Project Structure

- `views.py`: Contains function-based and class-based views
- `forms.py`: Blog and comment forms
- `models.py`: Blog, Comment, BlogLike, and CommentLike models
- `templates/`: HTML templates for rendering pages
