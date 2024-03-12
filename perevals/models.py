from django.db import models


class Pereval(models.Model):
    STATUS_CHOICES = [('NW', 'new'), ('PN', 'pending'), ('AC', 'accepted'),
                      ('RJ', 'rejected')]

    beauty_title = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    other_title = models.CharField(max_length=128)
    connect = models.CharField(max_length=128)
    add_time = models.CharField(max_length=128)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default='NW')

    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    coords = models.ForeignKey('Coords', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)


class Users(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    fam = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    otc = models.CharField(max_length=128)
    phone = models.CharField(max_length=64, unique=True)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=2, default="")
    summer = models.CharField(max_length=2, default="")
    autumn = models.CharField(max_length=2, default="")
    spring = models.CharField(max_length=2, default="")


class Images(models.Model):
    data = models.URLField(max_length=256)
    title = models.CharField(max_length=128)

    pereval = models.ForeignKey('Pereval', on_delete=models.CASCADE,
                                related_name='images')

    def __str__(self):
        return self.title
