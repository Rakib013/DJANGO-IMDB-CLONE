from django.contrib import admin
from . models import *

admin.site.register(Profile)
admin.site.register(Favorites)
admin.site.register(Comments)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'category', 'rating', 'language', 'year_of_production', 'views']
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ['rating', 'status', 'category', 'language']
    list_filter = ['category', 'status', 'rating', 'language']


@admin.register(MovieLinks)
class MovieLinkAdmin(admin.ModelAdmin):
    list_display = ['type', 'link']


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ['c_name', 'title', 'slug']
    list_filter = ['title', 'c_name']
    prepopulated_fields = {"slug": ('c_name',)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['title']
    prepopulated_fields = {"slug": ("title",)}

