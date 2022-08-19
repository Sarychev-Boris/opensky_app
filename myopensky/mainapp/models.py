from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Единственный действующий класс - воздушные суда, поля класса дублируют значения, получаемые посредсвтом OPENSKY API
# В дополнение к ним добавлено поле users, связанное с базовым классом django - User черезь связь ManyToMany
# для реализации 'любимых' ВС

class Airplane(models.Model):

    icao24 = models.CharField(max_length=40, primary_key=True)
    callsign = models.CharField(max_length=40, null=True, blank=True)
    origin_country = models.CharField(max_length=100)
    time_position = models.IntegerField(null=True, blank=True)
    last_contact = models.IntegerField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    baro_altitude = models.FloatField(null=True, blank=True)
    on_ground = models.BooleanField()
    velocity = models.FloatField(null=True, blank=True)
    true_track = models.FloatField(null=True, blank=True)
    vertical_rate = models.FloatField(null=True, blank=True)
    sensors = models.IntegerField(null=True, blank=True)
    geo_altitude = models.FloatField(null=True, blank=True)
    squawk = models.CharField(max_length=40, null=True, blank=True)
    spi = models.BooleanField()
    position_source = models.IntegerField()
    users = models.ManyToManyField(User, related_name='favorite')

    def __str__(self):
        return str([self.icao24, self.callsign, self.origin_country, self.longitude, self.latitude])

    def get_absolute_url(self):
        return reverse('airplane', kwargs={'icao24': self.icao24})

