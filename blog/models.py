from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        # Generate slug if not exists
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # First save (important for image path)
        super().save(*args, **kwargs)

        # Resize image if exists
        if self.image:
            img = Image.open(self.image.path)

            max_width = 800
            max_height = 800

            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                img.save(self.image.path)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.blog}"


class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blog", "user")


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")
