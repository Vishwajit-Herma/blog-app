# Blog Application

A Django-based blogging platform with authentication, CRUD blog management, comments, likes, notifications, and popularity tracking.

## Tech Stack

- Python
- Django 6.0.2
- SQLite
- Pillow (image processing)

## Current Features

- **Authentication**
  - Login, logout, and registration flows
  - Login required for blog features

- **Blog Management**
  - Create, list, detail, update, and delete blogs
  - Slug-based blog URLs
  - Author-only update/delete permissions
  - Edited-state tracking (`is_edited` + `updated_at`)

- **Media Support**
  - Optional blog image upload
  - Automatic image resize during save (max ~800x800)

- **Comments**
  - Add comments on blog detail page
  - Author-only comment deletion

- **Likes**
  - Like/unlike blogs
  - Like/unlike comments
  - Unique like constraints per user for blog/comment

- **View Tracking**
  - View count on blogs
  - Session-based unique increment to avoid repeated increments in same session

- **Notifications**
  - Notification records on:
    - New comments on your blog
    - New likes on your blog
    - New likes on your comment
  - Unread notification count in templates via context processor
  - Notifications marked as read when notification page is opened

- **Search & Pagination**
  - Search by blog title/content/author username
  - Paginated blog list

- **Popular Blogs**
  - Popular blogs page ordered by views
  - Implemented using proxy model

- **Daily Blog Creation Limit**
  - Middleware restricts authenticated users to max 5 blog posts/day

## Key Project Files

- [authent/blog/models.py](authent/blog/models.py)
- [authent/blog/views.py](authent/blog/views.py)
- [authent/blog/forms.py](authent/blog/forms.py)
- [authent/blog/urls.py](authent/blog/urls.py)
- [authent/blog/signals.py](authent/blog/signals.py)
- [authent/blog/middleware.py](authent/blog/middleware.py)
- [authent/blog/context_processors.py](authent/blog/context_processors.py)
- [authent/authent/settings.py](authent/authent/settings.py)
- [authent/authent/urls.py](authent/authent/urls.py)
- [authent/account/views.py](authent/account/views.py)

## Important Implementations (Reference)

- [`blog.models.Blog`](authent/blog/models.py)
- [`blog.models.Comment`](authent/blog/models.py)
- [`blog.models.BlogLike`](authent/blog/models.py)
- [`blog.models.CommentLike`](authent/blog/models.py)
- [`blog.models.Notification`](authent/blog/models.py)
- [`blog.models.PopularBlog`](authent/blog/models.py)
- [`blog.views.BlogListGenericView`](authent/blog/views.py)
- [`blog.views.BlogCreateView`](authent/blog/views.py)
- [`blog.views.BlogDetailView`](authent/blog/views.py)
- [`blog.views.BlogUpdateView`](authent/blog/views.py)
- [`blog.views.BlogDeleteView`](authent/blog/views.py)
- [`blog.views.toggle_blog_like`](authent/blog/views.py)
- [`blog.views.toggle_comment_like`](authent/blog/views.py)
- [`blog.views.notifications_view`](authent/blog/views.py)
- [`blog.views.PopularBlogListView`](authent/blog/views.py)
- [`blog.middleware.BlogCreationLimitMiddleware`](authent/blog/middleware.py)
- [`blog.context_processors.notification_count`](authent/blog/context_processors.py)

## Installation

From project root (`authent/`):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usage

1. Open `/account/register/` and create an account
2. Login at `/account/login/`
3. Create a blog at `/add/`
4. Browse all blogs at `/`
5. Open a blog detail page to:
   - add comments
   - like blog/comment
6. Check notifications at `/notifications/`
7. View popular blogs at `/popular/`

## URL Overview

- `/` → Blog list
- `/add/` → Create blog
- `/<slug>/` → Blog detail
- `/<slug>/update/` → Update blog
- `/<slug>/delete/` → Delete blog
- `/comment/<id>/delete/` → Delete comment
- `/<slug>/like/` → Toggle blog like
- `/comment/<id>/like/` → Toggle comment like
- `/notifications/` → Notifications
- `/popular/` → Popular blogs
- `/account/login/` `/account/logout/` `/account/register/`

## Notes

- Media files are served in development with `MEDIA_URL`/`MEDIA_ROOT`.
- Signals are loaded in app config (`BlogConfig.ready`).
- Current test files exist but are minimal:
  - [authent/blog/tests.py](authent/blog/tests.py)
  - [authent/account/tests.py](authent/account/tests.py)