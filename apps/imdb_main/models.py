from django.db import models
'''
Model to store persons related to movie
'''

class Person(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name

'''
Model to store genres
'''
class Genre(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

'''
Model to store  movie
'''
class Movie(models.Model):
    name=models.CharField(max_length=150)
    imdb_score=models.FloatField(default=0.0)
    popularity99=models.FloatField(verbose_name='99popularity',help_text='99popularity',default=0.0)
    people=models.ManyToManyField(Person,through='MoviePersonRoles')
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name
class MovieRole(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MoviePersonRoles(models.Model):
    person=models.ForeignKey(Person,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role= models.ForeignKey(MovieRole, on_delete=models.CASCADE)