from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


from .forms import BlogForm, CommentForm
from .models import Blog, Comment, CommentLike, BlogLike, Notification, PopularBlog


@login_required
def blog_list(request):
    # blogs = Blog.objects.all().order_by("-created_at")
    blogs = Blog.objects.select_related("author").order_by("-created_at")

    return render(request, "blog/blog_list.html", {"blogs": blogs})


class BlogListGenericView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"
    paginate_by = 5

    def get_queryset(self):
        queryset = Blog.objects.select_related("author").order_by("-created_at")

        query = self.request.GET.get("q", "").strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(author__username__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class BlogListView(LoginRequiredMixin, View):

    def get(self, request):
        blogs = Blog.objects.select_related("author").order_by("-created_at")
        return render(request, "blog/blog_list.html", {"blogs": blogs})


# ---------------------------------------------------------------------------


@login_required
def blog_create(request):

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("blog:blog-list")
    else:
        form = BlogForm()

    return render(request, "blog/blog_add.html", {"form": form})


class BlogCreateGenericView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "blog/blog_add.html"
    success_url = reverse_lazy("blog:blog-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = BlogForm()
        return render(request, "blog/blog_add.html", {"form": form})

    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("blog:blog-list")
        return render(request, "blog/blog_add.html", {"form": form})


# ---------------------------------------------------------------------------


@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # Increment views safely
    Blog.objects.filter(pk=blog.pk).update(views=F("views") + 1)
    blog.refresh_from_db()

    return render(request, "blog/blog_detail.html", {"blog": blog})


class BlogDetailGenericView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        viewed_key = f"viewed_blog_{obj.pk}"

        if not self.request.session.get(viewed_key):
            Blog.objects.filter(pk=obj.pk).update(views=F("views") + 1)
            self.request.session[viewed_key] = True

        obj.refresh_from_db()
        return obj


class BlogDetailView(LoginRequiredMixin, View):

    def get(self, request, slug):
        blog = get_object_or_404(
            Blog.objects.prefetch_related("comments__user"), slug=slug
        )

        # Unique session key for this blog
        viewed_key = f"viewed_blog_{blog.pk}"

        # Only increment if not viewed in this session
        if not request.session.get(viewed_key):
            Blog.objects.filter(pk=blog.pk).update(views=F("views") + 1)
            request.session[viewed_key] = True
            blog.refresh_from_db()  # So updated value shows immediately

        form = CommentForm()

        return render(request, "blog/blog_detail.html", {"blog": blog, "form": form})

    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()

            return redirect("blog:blog-detail", slug=slug)

        return render(request, "blog/blog_detail.html", {"blog": blog, "form": form})


# ---------------------------------------------------------------------------


@login_required
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            updated_blog = form.save(commit=False)
            updated_blog.is_edited = True
            updated_blog.save()
            return redirect("blog:blog-list")
    else:
        form = BlogForm(instance=blog)

    return render(request, "blog/blog_update.html", {"form": form})


class BlogUpdateGenericView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "blog/blog_update.html"
    success_url = reverse_lazy("blog:blog-list")

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.is_edited = True
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, View):

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, author=request.user)
        form = BlogForm(instance=blog)
        return render(request, "blog/blog_update.html", {"form": form})

    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, author=request.user)
        form = BlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            updated_blog = form.save(commit=False)
            updated_blog.is_edited = True
            updated_blog.save()
            return redirect("blog:blog-list")

        return render(request, "blog/blog_update.html", {"form": form})


# ---------------------------------------------------------------------------


@login_required
def blog_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)
    if request.method == "POST":
        blog.delete()
        return redirect("blog:blog-list")

    return render(request, "blog/blog_delete.html", {"blog": blog})


class BlogDeleteGenericView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "blog/blog_delete.html"
    success_url = reverse_lazy("blog:blog-list")

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)


class BlogDeleteView(LoginRequiredMixin, View):

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, author=request.user)
        return render(request, "blog/blog_delete.html", {"blog": blog})

    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, author=request.user)
        blog.delete()
        return redirect("blog:blog-list")


# ------------------------------------------------------------------------------------------------------


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    blog_slug = comment.blog.slug
    comment.delete()
    return redirect("blog:blog-detail", slug=blog_slug)


@login_required
def toggle_blog_like(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    like, created = BlogLike.objects.get_or_create(blog=blog, user=request.user)

    if not created:
        like.delete()

    return redirect("blog:blog-detail", slug=slug)


@login_required
def toggle_comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    like, created = CommentLike.objects.get_or_create(
        comment=comment, user=request.user
    )

    if not created:
        like.delete()

    return redirect("blog:blog-detail", slug=comment.blog.slug)


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )

    # Get unread IDs first
    unread_ids = notifications.filter(is_read=False).values_list("id", flat=True)

    response = render(
        request,
        "blog/notifications.html",
        {"notifications": notifications},
    )

    # Mark them as read AFTER preparing response
    Notification.objects.filter(id__in=unread_ids).update(is_read=True)

    return response



class PopularBlogListView(ListView):
    model = PopularBlog
    template_name = "blog/popular_blogs.html"
    context_object_name = "blogs"   