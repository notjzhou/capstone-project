from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator

# Values taken from https://colemizestudios.com/how-to-rap-picking-rap-beats-to-flow-on/
# Create your models here.


class Beat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='audio/beats', validators=[FileExtensionValidator(['wav', 'mp3'])])
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    SLOW_LOWER = 65
    MID_LOWER = 85
    FAST_LOWER = 120

    SLOW_UPPER = 75
    MID_UPPER = 95
    FAST_UPPER = 200

    BEAT_TEMPO_CHOICES = [
        (SLOW_LOWER, 'Slow'),
        (MID_LOWER, 'Mid'),
        (FAST_LOWER, 'Fast'),
    ]

    bpm = models.PositiveSmallIntegerField(validators=[MinValueValidator(SLOW_LOWER), MaxValueValidator(FAST_UPPER)])

    def __str__(self):
        return self.name

    def is_slow(self):
        return self.bpm >= self.SLOW_LOWER and self.bpm <= self.SLOW_UPPER

    def is_mid(self):
        return self.bpm >= self.MID_LOWER and self.bpm <= self.MID_UPPER

    def is_fast(self):
        return self.bpm >= self.FAST_LOWER and self.bpm <= self.FAST_UPPER

    # currently just a simple wav file
    # switch to https://github.com/areski/django-audiofield if required for upload
    # NOTE - installed the above repo, kinda outdated


class Rap(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bpm = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    recording = models.FileField(upload_to='audio/raps')
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
