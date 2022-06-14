from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Response
from django.urls import reverse_lazy, reverse
from .forms import ResponseForm


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    form_class = ResponseForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = ResponseForm(
            initial={'post': self.object, 'user': self.request.user})
        context['accepted_responses'] = Response.objects.filter(
            status=True, post__id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    fields = ['title', 'text', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ['title', 'text', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/profile.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'posts/response_list.html'

    def get_queryset(self, **kwargs):
        return Response.objects.filter(post__user=self.request.user, post__id=self.kwargs['pk'])


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'posts/response_delete.html'
    success_url = reverse_lazy('profile')


class ResponseUpdateView(LoginRequiredMixin, UpdateView):
    model = Response
    template_name = 'posts/response_update.html'
    fields = ['status', ]
    success_url = reverse_lazy('profile')
