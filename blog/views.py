from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import post
from django.views.generic import(
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)

posted = [
	{
		'author': 'nasha',
		'title': 'pasha-post',
		'content': 'first post'
	},
	{
		'author': 'badshah',
		'title': 'masala-post',
		'content': 'second post'
	}
]

def home(request):
	context={
		'posts': post.objects.all()
	}
	return render(request,'blog/home.html',context)

def about(request):
	return render(request,'blog/about.html',{'title': 'COD-abouts'})

def testBootstrap(request):
	return render(request,'blog/test_bootstrap.html',{'title': 'bootstrap-testing'})

class PostListView(ListView):
	model=post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	paginate_by = 5

class PostDetailView(DetailView):
	model=post

class PostCreateView(LoginRequiredMixin, CreateView):
	model=post
	fields = ['title' , 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
	model=post
	template_name = 'blog/post_update.html'
	fields = ['title' , 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		post=self.get_object()
		if self.request.user== post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
	model=post
	success_url = '/'

	def test_func(self):
		post=self.get_object()
		if self.request.user== post.author:
			return True
		return False