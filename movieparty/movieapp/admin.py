from django.contrib import admin
from .models import Movie, Room, Genre, Country, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    filter_horizontal = ('country', 'genre')
    list_display = ('title', 'year', 'get_image_html')
    inlines = [RatingInline]
    list_per_page = 5
    ordering = ('-year',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Room)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Rating)
