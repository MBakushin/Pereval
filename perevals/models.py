from django.db import models


class Pereval(models.Model):
    STATUS_CHOICES = [('NW', 'new'), ('PN', 'pending'), ('AC', 'accepted'),
                      ('RJ', 'rejected')]

    beauty_title = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    other_title = models.CharField(max_length=128, null=True, blank=True)
    connect = models.CharField(max_length=128, null=True, blank=True, default="")
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default='NW')

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    coords = models.ForeignKey('Coords', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class User(models.Model):
    email = models.EmailField(max_length=128)
    fam = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    otc = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=64)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=2, null=True, blank=True, default="")
    summer = models.CharField(max_length=2, null=True, blank=True,  default="")
    autumn = models.CharField(max_length=2, null=True, blank=True, default="")
    spring = models.CharField(max_length=2, null=True, blank=True, default="")


class Images(models.Model):
    data = models.ImageField(upload_to='images')
    title = models.CharField(max_length=128)

    pereval = models.ForeignKey('Pereval', on_delete=models.CASCADE,
                                related_name='images')

    def __str__(self):
        return self.title
