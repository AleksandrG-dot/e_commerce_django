from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.models import BlogPost


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.kwargs.get("pk")])


class BlogListView(ListView):
    model = BlogPost

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = "blog"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog:blog_list")
