from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.imdb_main.models import *
import os, json


class Command(BaseCommand):
    help = 'load fixtures'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, 'imdb.json')

        mov_role = MovieRole(name='director')
        mov_role.save()
        with open(file) as data_file:
            movie_list = json.load(data_file)
        for movie in movie_list:
            mov = Movie(name=movie["name"], imdb_score=movie["imdb_score"], popularity99=movie["99popularity"])
            people = Person.objects.get_or_create(name=movie["director"])[0]
            mov.save()

            mov_p_roles = MoviePersonRoles(person=people, movie=mov, role=mov_role)
            mov_p_roles.save()
            for genre in movie['genre']:
                mov_genre = Genre.objects.get_or_create(name=genre)[0]
                mov.genre.add(mov_genre)
            mov.save()

            print(movie)
