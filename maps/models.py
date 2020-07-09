from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.conf import settings


class VectorLayer(models.Model):
    name = models.CharField(max_length=50)
    dataUrl = models.CharField(
        max_length=200,
        blank=True,
        help_text='Complete path including querystring if any. For local files in "data" directory, must prefix filename with "/static/data/"'
    )
    dataSuffix = models.CharField(
        max_length=12,
        blank=True,
        help_text='Enter filetype suffix without the period: wkt, geojson, csv, kml, topojson, gpx'
    )
    description = models.TextField(blank=True)

    def vector_default_style():
        return dict({
            "radius": 6,
            "fillColor": "#ff0",
            "color": "#f00",
            "weight": 1,
            "opacity": 1,
            "fillOpacity": 0.7,
        })

    style = JSONField(blank=True, null=True, default=vector_default_style,
                      help_text='key-value pairs for styling')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'vectors'


class RasterLayer(models.Model):
    name = models.CharField(max_length=50)
    tileUrl = models.CharField(
        max_length=200,
        blank=True,
        help_text='Add tileset URL here, such as https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    )

    def raster_default_attrs():
        return dict({
            "maxZoom": 15,
            "attribution": "None",
            "id": "None",
            "accessToken": "None"
        })

    attrs = JSONField(
        null=True,
        blank=True,
        default=raster_default_attrs,
        help_text='Insert desired fields/values or required by tileset provider here.')

    def __str__(self):
        return self.name

    class Meta:
        # ordering may interfere with layer order on map
        verbose_name_plural = 'rasters'


class Map(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            help_text='give map descriptive and unique name')
    description = models.TextField(blank=True,
                                   help_text='describe map and purpose')
    entered = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.CustomUser',
                               null=True, blank=True, related_name='map_author',
                               on_delete=models.SET_NULL)
    center = ArrayField(models.FloatField(default=15),
                        size=2,
                        default=list,
                        help_text="latitude, longitude in decimal degrees")
    zoom = models.IntegerField(default=8, help_text="initial zoom level")
    rasters = models.ManyToManyField(RasterLayer, blank=True)
    vectors = models.ManyToManyField(VectorLayer, blank=True)

    def __str__(self):
        return "%s map posted on %s" % (self.name, self.entered.date())

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'maps'
