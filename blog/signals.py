from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification, BlogLike, CommentLike


@receiver(post_save, sender=Comment)
def notify_author_on_comment(sender, instance, created, **kwargs):
    if created and instance.user != instance.blog.author:
        Notification.objects.create(
            user=instance.blog.author,
            message=f"{instance.user.username} commented on your blog.",
        )


@receiver(post_save, sender=BlogLike)
def notify_author_on_like(sender, instance, created, **kwargs):
    if created and instance.user != instance.blog.author:
        Notification.objects.create(
            user=instance.blog.author,
            message=f"{instance.user.username} liked your blog."
        )


@receiver(post_save, sender=CommentLike)
def notify_author_on_comment_like(sender, instance, created, **kwargs):

    if created and instance.user != instance.comment.user:
        Notification.objects.create(
            user=instance.comment.user,
            message=f"{instance.user.username} liked your comment."
        )
