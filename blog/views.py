from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.models import BlogPost


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy('blog:blog_list')


class BlogListView(ListView):
    model = BlogPost

class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = 'blog'


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:blog_list')
