from django.contrib import admin
from .models import Movie, Room, Genre, Country, Rating, Review


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    collapse = True


class MovieAdmin(admin.ModelAdmin):
    filter_horizontal = ('country', 'genre')
    list_display = ('title', 'year', 'get_image_html')
    inlines = [RatingInline]
    list_per_page = 5
    ordering = ('-year',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    list_per_page = 20


class GenreAdmin(admin.ModelAdmin):
    list_per_page = 20


class CountryAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Movie, MovieAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Review)
