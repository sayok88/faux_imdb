from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

def request_validator(request, check_list):
    try:
        data = request.data
        for field in check_list:
            if field not in data:
                return False
    except Exception as e:
        return False
    return True


class CustomView(APIView):
    """
    custom dispatch to check post data params
    """
    required_params = []

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            if request.method.lower() == "post" and not request_validator(request, self.required_params):

                response = Response(
                    'parameters mising',
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class LoginView(CustomView):
    required_params = ['user', 'password']

    def post(self, request, format=None):
        try:
            user = request.data["user"]
            password = request.data["password"]
            user = authenticate(username=user, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    Token.objects.get_or_create(user=user)
                    return Response({"success": True, "Token": Token})
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})


class AddMovieView(CustomView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    required_params = ['name', 'imdb_score', '99popularity', 'ratings', 'people', 'genre']

    def post(self, request, format=None):
        data = request.data
        try:
            movie = Movie(name=data["name"], imdb_score=data["imdb_score"], popularity99=data['99popularity'])
            movie.save()
            for person in data["people"]:
                role = MovieRole.objects.get_or_create(name=person["role"])[0]
                person_temp = Person.objects.get_or_create(name=person["name"])[0]
                mov_p_roles = MoviePersonRoles(person=person_temp, movie=movie, role=role)
                mov_p_roles.save()
            for tag in data["genre"]:
                genre = Genre.objects.get_or_create(name=tag)
                movie.genre.add(genre)
            movie.save()
            return Response({'movie_id': movie.pk})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteMovieView(CustomView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    required_params = ['id']

    def post(self, request, format=None):
        try:
            Movie.objects.filter(pk=int(request.data['id'])).delete()
            return Response({'message': 'success'})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EditMovieView(CustomView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    required_params = ['id', 'name', 'imdb_score', '99popularity',
                       'ratings','delete_genre','add_genre','delete_movie_person','edit_person_role','add_person']

    def post(self, request, format=None):
        try:
            data = request.data
            movie = Movie.objects.get(id=data['id'])
            movie.name = data['name']
            movie.imdb_score = data['imdb_score']
            movie.popularity99 = data['99popularity']
            for tag in data["delete_genre"]:
                genre=Genre.objects.filter(name=tag)
                if genre:
                    genre=genre.first()
                    if genre in movie.genre.all():
                        movie.genre.remove(genre)

            for tag in data["add_genre"]:
                genre = Genre.objects.get_or_create(name=tag)[0]
                if genre not in movie.genre.all():
                    movie.genre.add(genre)
            for movieperson in data["delete_movie_person"]:
                if 'id' in  movieperson.keys():
                    person = Person.objects.filter(id=int(movieperson["id"]))
                    if person:
                        person=person.first()
                        if 'role' in movieperson.keys():
                            role=MovieRole.objects.filter(name=movieperson["role"])
                            if role:
                                role=role.first()
                                MoviePersonRoles.objects.filter(person=person,role=role,movie=movie).delete()
                        else:
                            MoviePersonRoles.objects.filter(person=person, movie=movie).delete()
                else:
                    if 'name' in movieperson.keys():
                        person=Person.objects.filter(name=movieperson["name"])
                        if person:
                            person = person.first()
                            if 'role' in movieperson.keys():
                                role = MovieRole.objects.filter(name=movieperson["role"])
                                if role:
                                    role = role.first()
                                    MoviePersonRoles.objects.filter(person=person, role=role, movie=movie).delete()
                            else:
                                MoviePersonRoles.objects.filter(person=person, movie=movie).delete()

            for movieperson in data['edit_person']:
                person=None
                if 'id' in movieperson.keys():
                    person=Person.objects.filter(id=int(movieperson['id']))
                    if person:
                        person.first()
                else:
                    if 'name' in movieperson.keys():
                        person = Person.objects.filter(name=movieperson['name'])
                        if person:
                            person.first()
                if person:
                    if 'prev_role' in movieperson.keys():
                        prev_role = MovieRole.objects.filter(name=movieperson["prev_role"])
                        if prev_role:
                            prev_role=prev_role.first()
                            if 'new_role' in movieperson.keys():
                                new_role=MovieRole.objects.get_or_create(name=movieperson['new_role'])[0]
                                moviepersonrole=MoviePersonRoles.objects.filter(movie=movie,person=person,role=prev_role)
                                if moviepersonrole and not MoviePersonRoles.objects.filter(movie=movie,person=person,role=new_role).exists():
                                    moviepersonrole=moviepersonrole.first()
                                    moviepersonrole.role=new_role
                                    moviepersonrole.save()

            for movieperson in data['add_person']:
                person = None
                if 'id' in movieperson.keys():
                    person = Person.objects.filter(id=int(movieperson['id']))
                    if person:
                        person.first()
                else:
                    if 'name' in movieperson.keys():
                        person = Person.objects.filter(name=movieperson['name'])
                        if person:
                            person.first()
                if 'role' in movieperson.keys():
                    role = MovieRole.objects.get_or_create(name=movieperson['role'])[0]
                    if not MoviePersonRoles.objects.filter(movie=movie,person=person,role=role).exists():
                        MoviePersonRoles(movie=movie, person=person, role=role).save()



            movie.save()
            return Response({'message': 'success'})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving movies.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
    permission_classes = ()


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving movies.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = ()

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = ()


    # def list(self, request):
    #
    #     serializer = MovieSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Movie.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     (user)
    #     return Response(serializer.data)


class SearchView(CustomView):
    required_params =  ['search']
    permission_classes = ()
    def post(self,request,format=None):
        movies=Movie.objects.filter(name__icontains=request.data['search'].lower())
        person = Person.objects.filter(name__icontains=request.data['search'].lower())
        genre = Genre.objects.filter(name__icontains=request.data['search'].lower())
        movie_serializer=MovieSerializer(movies,many=True)
        person_serializer=PersonSerializer(person,many=True)
        genre_serializer = GenreModelSerializer(genre,many=True)
        return Response({'movies':movie_serializer.data,'person':person_serializer.data,'genre':genre_serializer.data})
