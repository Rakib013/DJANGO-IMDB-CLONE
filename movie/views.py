from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from . models import Movie as MovieModel, MovieLinks, Celebrity as CelebrityModel, Blog as BlogModel, Favorites, Profile as ProfileModel
from django.contrib import messages
from . forms import *


class Movies(ListView):
    model = MovieModel
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(Movies, self).get_context_data(**kwargs)
        return context


class Movie(DetailView):
    model = MovieModel

    def get_object(self):
        object = super(Movie, self).get_object()
        object.views += 1
        object.save()
        return object

    def get_context_data(self, **kwargs):
        context = super(Movie, self).get_context_data(**kwargs)
        context['links'] = MovieLinks.objects.filter(movie=self.get_object())
        context['related_movies'] = MovieModel.objects.filter(category=self.get_object().category)
        return context


class MovieCategory(ListView):
    template_name = "movie/movie_category.html"

    def get_queryset(self):
        self.category = self.kwargs['category']
        return MovieModel.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(MovieCategory, self).get_context_data(**kwargs)
        context['movie_category'] = self.category
        return context


class MovieLanguage(ListView):
    template_name = "movie/movie_category.html"

    def get_queryset(self):
        self.language = self.kwargs['language']
        return MovieModel.objects.filter(language=self.language)

    def get_context_data(self, **kwargs):
        context = super(MovieLanguage, self).get_context_data(**kwargs)
        context['movie_language'] = self.language
        return context


class MovieStatus(ListView):
    template_name = "movie/home.html"

    def get_queryset(self):
        self.status = self.kwargs['status']
        return MovieModel.objects.filter(status=self.status)
    
    def get_context_data(self, **kwargs):
        context = super(MovieStatus, self).get_context_data(**kwargs)
        context['movie_status'] = self.get_queryset()
        context['status'] = self.status
        return context


class MovieBanner(ListView):
    model = MovieModel
    template_name = "movie/home.html"

    def get_context_data(self, **kwargs):
        context = super(MovieBanner, self).get_context_data(**kwargs)
        context["movie_banner"] = MovieModel.objects.filter(status="coming soon")
        context["all_movies"] = MovieModel.objects.all()
        context['spot_celebrity'] = CelebrityModel.objects.all()
        return context
    

class MovieSearch(ListView):
    model = MovieModel

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)

        else:
            object_list = self.model.objects.none()

        return object_list


class UserRegister(View):
    def post(self, *args, **kwargs):
        form = RegistrationForm(self.request.POST or None)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                ProfileModel.objects.create(user=user)
                login(self.request, user)
                return redirect("home")
            except:
                return redirect("404.html")


class UserUpdate(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        form = InfoUpdate(instance=self.request.user, data=self.request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                return redirect("profile")
            except:
                return redirect("404.html")
                    
        else:
            form = InfoUpdate(instance=self.request.user)
            return redirect("profile")


class MyLoginView(LoginView):
    form = MyAuthForm
        

class PasswordUpdate(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = Password_update(instance=self.request.user, data=self.request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect("profile")
            except:
                return redirect("404.html")
        
        else:
            form = Password_update(instance=self.request.user)
            return redirect("profile")


class Profile_pic_update(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = PicUpdate(files=self.request.FILES, instance=self.request.user.profile, data=self.request.POST)
        if form.is_valid():
           profile = form.save(commit=False)
           profile.save()
           return redirect("profile")

        else:
            form = PicUpdate(instance=self.request.user)
            return redirect("profile")


class Profile(ListView, LoginRequiredMixin):
    template_name = "movie/profile.html"
    model = ProfileModel

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['profile'] = ProfileModel.objects.get(user=self.request.user)
        return context


def series(request):
    return render(request, 'movie/series.html')


class Celebritys(ListView):
    model = CelebrityModel
    template_name = "movie/celebritys.html"


class Celebrity(DetailView):
    model = CelebrityModel
    template_name = "movie/celebrity.html"


class Blogs(ListView):
    model = BlogModel
    template_name = "movie/blogs.html"


class Blog(DetailView):
    model = BlogModel
    template_name = "movie/blog.html"

    def get_object(self):
        object = super(Blog, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(Blog, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(blogs__slug=self.get_object().slug)
        return context



class NewsComment(View, LoginRequiredMixin):
    def post(self, request, slug, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.blogs = get_object_or_404(BlogModel, slug=slug)
            comment.profile = get_object_or_404(ProfileModel, user=request.user)
            comment.save()
            return redirect("blog", slug)
        else:
            form = CommentForm()
            return redirect("blog", slug)


class Favorite(ListView):
    model = Favorites
    template_name = "movie/favorites.html"

    def get_context_data(self, **kwargs):
        context = super(Favorite, self).get_context_data(**kwargs)
        favorites = Favorites.objects.filter(user=self.request.user)
        if favorites.exists():
            favorite = favorites[0]
        else:
            favorite = Favorites.objects.create(user=self.request.user)
        context["favorite_movies"] = favorite.movies.all()
        return context


@login_required
def add_to_favorites(request, slug):
    movie = get_object_or_404(MovieModel, slug=slug)
    favorites = Favorites.objects.filter(user=request.user)
   
    if favorites.exists():
        favorite = favorites[0]
        if favorite.movies.filter(slug=movie.slug).exists():
            messages.info(request, f"{movie.title} is already in your favorite")
            return redirect("favorites")
        else:
            favorite.movies.add(movie)
            messages.info(request, f"{movie.title} added to your favorite")
            return redirect("favorites")
    else:
        favorite = Favorites.objects.create(user=request.user)
        favorite.movies.add(movie)
        messages.info(request, "Movie added to your favorite")
        return redirect("favorites")



def rate(request):
    return render(request, 'movie/rate.html')

def error(request):
    return render(request, 'movie/404.html')

def comingsoon(request):
    return render(request, 'movie/comingsoon.html')