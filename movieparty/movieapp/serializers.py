from rest_framework import serializers

from .models import Movie, Genre, Country, Room


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all(), many=True)
    genre = serializers.SlugRelatedField(slug_field='name', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        # Получаем связанные объекты Country и Genre по их именам
        country_names = validated_data.pop('country')
        genre_names = validated_data.pop('genre')
        countries = Country.objects.filter(name__in=country_names)
        genres = Genre.objects.filter(name__in=genre_names)

        # Создаем фильм
        movie = Movie.objects.create(**validated_data)

        # Связываем фильм с выбранными странами и жанрами
        movie.country.set(countries)
        movie.genre.set(genres)
        return movie


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
