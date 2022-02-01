"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: Publishing of Posts and Management of Posts
"""
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import redirect, render, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from evangelism.models import Member, Minister, Ministry
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from users.models import User

from .forms import CommentForm, PostForm
from .models import Author, Post, PostView

form = EmailSignupForm()


def get_author(user):
    """collects the author from the model"""
    query = Author.objects.filter(user=user)
    if query.exists():
        return query[0]
    return None


class SearchView(View):
    """this feature is meant to search through a variety of content"""

    def get(self, request):
        """this feature is meant to search through a variety of content"""
        queryset = Post.objects.all()
        query = request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(overview__icontains=query)
            ).distinct()
        context = {"queryset": queryset}
        return render(request, "search_results.html", context)


def search(request):
    """this feature is meant to search through a variety of content"""
    queryset = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        ).distinct()
    context = {"queryset": queryset}
    return render(request, "search_results.html", context)


def get_category_count():
    """this feature is meant to return how many categories belonging to a post"""
    queryset = Post.objects.values("categories__title").annotate(
        Count("categories__title")
    )
    return queryset


class IndexView(View):
    """this class returns for us the home view"""

    form = EmailSignupForm()

    def get(self, request):
        """this function returns featured posts, and activation of accounts"""
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by("-timestamp")[0:3]
        context = {"object_list": featured, "latest": latest, "form": self.form}
        # also we open a members account too once is completed registering
        try:
            confirm_email = self.request.GET.get("confirm_email")
            member_pk = self.request.GET.get("member")
            minister_pk = self.request.GET.get("minister")
            ministry_pk = self.request.GET.get("ministry")
        except ObjectDoesNotExist as message_:
            messages.error(self.request, message=message_)

        instance = Member.objects.filter(pk=member_pk)
        minister_instance = Minister.objects.filter(pk=minister_pk)
        ministry_instance = Ministry.objects.filter(pk=ministry_pk)

        if confirm_email:
            if instance.exists():
                instance = instance.first()
            elif minister_instance.exists():
                instance = minister_instance.first()
            else:
                instance = ministry_instance.first()
            user = User()
            user.username = instance.name
            user.email = instance.email
            user.password = instance.password
            user.is_member = True
            user.save()
            messages.success(
                self.request,
                message="You have successfully activated an account with Laylinks",
            )
            return redirect("/")

        return render(request, "index.html", context)

    def post(self, request):
        """this function signs up an individual and allocates him/her a subscription"""
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")


def about(request):
    """this function simply returns the about us page"""
    context = {
        "about": True,
    }
    return render(request, "about.html", context)


class PostListView(ListView):
    """this class returns a list of posts"""

    form = EmailSignupForm()
    model = Post
    template_name = "blog.html"
    context_object_name = "queryset"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        """this function does further filter on the posts as they are being listed"""
        category_count = get_category_count()
        most_recent = Post.objects.order_by("-timestamp")[:3]
        context = super().get_context_data(**kwargs)
        context["most_recent"] = most_recent
        context["page_request_var"] = "page"
        context["category_count"] = category_count
        context["form"] = self.form
        return context


class PostDetailView(DetailView):
    """this class returns the details of each post"""

    model = Post
    template_name = "post.html"
    context_object_name = "post"
    form = CommentForm()

    def get_object(self):
        """this function returns the post as an object"""
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=obj)
        return obj

    def get_context_data(self, **kwargs):
        """this function does further filtering on the posts"""
        category_count = get_category_count()
        most_recent = Post.objects.order_by("-timestamp")[:3]
        context = super().get_context_data(**kwargs)
        context["most_recent"] = most_recent
        context["page_request_var"] = "page"
        context["category_count"] = category_count
        context["form"] = self.form
        return context

    def post(self, request):
        """this function allows for addition of comments"""
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={"pk": post.pk}))
        return None


class PostCreateView(CreateView):
    """this class creates a brand new post"""

    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        """this function returns the create flag"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context

    def form_valid(self, form):
        """this function saves the data obtained from the form"""
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={"pk": form.instance.pk}))


class PostUpdateView(UpdateView):
    """this class is meant to update a post"""

    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        """this function returns the update flag"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Update"
        return context

    def form_valid(self, form):
        """this function is the one that does the literal saving"""
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={"pk": form.instance.pk}))


class PostDeleteView(DeleteView):
    """this class deletes a post"""

    model = Post
    success_url = "/blog"
    template_name = "post_confirm_delete.html"
