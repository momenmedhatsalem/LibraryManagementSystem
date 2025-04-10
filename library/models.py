from django.db import models
from django.contrib.gis.db import models as gis_models


class Library(models.Model):
    name = models.CharField(max_length=255)
    # Can be changed to GPS coordinates
    location = gis_models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
