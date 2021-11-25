from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

CATEGORY_CHOICES = (
    ('action', 'ACTION'),
    ('adventure', 'ADVENTURE'),
    ('comedy', 'COMEDY'),
    ('drama', 'DRAMA'),
    ('romantic', 'ROMANTIC'),
    ('horror', 'HORROR'),
    ('thriller', 'THRILLER'),
    ('survivour', 'SURVIVOUR'),
    ('scifi', 'SCI-FI')
)

LANGUAGE_CHOICES = (
    ('english', 'ENGLISH'),
    ('bangla', 'BANGLA')
)

STATUS_CHOICES = (
    ('recently added', 'RECENTLY ADDED'),
    ('most watched', 'MOST WATCHED'),
    ('popular', 'POPULAR'),
    ('coming soon', 'COMING SOON'),
    ('top rated', 'TOP RATED')
)

LINK_CHOICES = (
    ('D', 'DOWNLOAD'),
    ('W', 'WATCH')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="profile/pic", default='profile/Default.jpeg', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="movies")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    year_of_production = models.DateField()
    views = models.IntegerField(default=0)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie", kwargs={"pk": self.pk})
    

class MovieLinks(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_link")
    type = models.CharField(choices=LINK_CHOICES, max_length=1)
    link = models.URLField()

    def __str__(self):
        return self.movie.title
    

class Celebrity(models.Model):
    c_name = models.CharField(max_length=20)
    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to="celebrity", null=True)
    slug = models.SlugField(unique=True)
    job = models.CharField(max_length=10)
    overview = models.TextField()
    biography = models.TextField()

    def __str__(self):
        return self.c_name

    def get_absolute_url(self):
        return reverse("celebrity", kwargs={"slug": self.slug})


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumb_img = models.ImageField(upload_to="blogs/thumbnil_img")
    title_img = models.ImageField(upload_to="blogs/title_img")
    blog = models.TextField()
    detail_img1 = models.ImageField(upload_to="blogs/detail_image", null=True, blank=True)
    detail_img2 = models.ImageField(upload_to="blogs/detail_image", null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog", kwargs={"slug": self.slug})


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " favorites movie list."


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    blogs = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.blogs.blog
    
    