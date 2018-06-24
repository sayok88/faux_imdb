'''

Serializers

'''

from rest_framework import serializers

from apps.imdb_main.models import Movie, MoviePersonRoles, Genre, Person
'''
All Genres
'''
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

'''
Get role name, person name and person id
'''
class MovieRoleSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(source='role.name')

    name = serializers.ReadOnlyField(source='person.name')

    id = serializers.ReadOnlyField(source='person.id')

    class Meta:
        model = MoviePersonRoles

        fields = ('name', 'role', 'id')


class MovieRoleNameSerializer(serializers.ModelSerializer):
    movie = serializers.ReadOnlyField(source='movie.name')
    movie_id = serializers.ReadOnlyField(source='movie.id')
    role = serializers.ReadOnlyField(source='role.name')

    class Meta:
        model = MoviePersonRoles

        fields = ('movie', 'movie_id', 'role')


# class GenreS
class MovieSerializer(serializers.ModelSerializer):
    people = MovieRoleSerializer(source='moviepersonroles_set', many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1


class PersonSerializer(serializers.ModelSerializer):
    movie = MovieRoleNameSerializer(source='moviepersonroles_set', many=True, read_only=True)

    class Meta:
        model = Person
        fields = ('id', 'name', 'movie')


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name')


class GenreModelSerializer(serializers.ModelSerializer):
    movie = MovieGenreSerializer(source='movie_set', many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ('id', 'name', 'movie')
