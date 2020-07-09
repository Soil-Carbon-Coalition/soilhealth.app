"""
This enables you to load a csv file of points into a point model

Once things are good, in the Django shell import this file and run point_load()
"""
from django.contrib.gis import geos
from obs.models import PointSite

point_csv = os.path.abspath(os.path.join('data', 'points.csv'))


def point_load():
    with open(point_csv) as point_file:
        for line in point_file:
            name, lon, lat = line.split(',')
            point = "POINT(%s %s)" % (lon.strip(), lat.strip())
            PointSite.objects.create(name=name, geom=geos.fromstr(point))
