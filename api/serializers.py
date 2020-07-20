from obs.models import Site, Observation, Project
from obs.filters import filter_site_observations
from maps.models import Map, RasterLayer, VectorLayer
from users.models import CustomUser, UserStatus
from resources.models import Resource
from upload.models import File
from rest_framework import serializers
from django.db.models.functions import Length
# this one formats as geojson:
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


# from https://github.com/wq/wq.db/blob/master/rest/serializers.py
class GeometryField(serializers.Field):
    def to_representation(self, value):
        if value is None:
            return None
        import json
        return json.loads(value.geojson)

    def to_internal_value(self, value):
        import json
        if isinstance(value, dict):
            value = json.dumps(value)

        if not GEOSGeometry:
            raise Exception("Missing GDAL")

        geom = GEOSGeometry(value)
        srid = getattr(settings, 'SRID', 4326)

        if 'crs' in value and value['crs'].get('type', None) == 'name':
            name = value['crs']['properties']['name']
            if name.startswith('urn:ogc:def:crs:EPSG::'):
                geom.srid = int(name.replace('urn:ogc:def:crs:EPSG::', ''))

        if geom.srid is None:
            geom.srid = 4326
        if geom.srid != srid:
            geom.transform(srid)
        return geom


class ObsSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.__str__()

    class Meta:
        model = Observation
        fields = ('id', 'label', 'project', 'type', 'observer', 'site', 'kv')


class Obs2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Observation
        fields = ('__all__')


# THIS ONE YIELDS GEOJSON!!
class ObsGeoSerializer(GeoFeatureModelSerializer):
    # get and format geometry field from Site model
    geometry = GeometryField(
        source='site.geometry',
        read_only=True,
    )
    # get site name from Site model
    Site = serializers.ReadOnlyField(
        source='site.name',
    )
    Label = serializers.SerializerMethodField()

    def get_Label(self, obj):
        return obj.__str__()

    Observer = serializers.ReadOnlyField(
        source='observer.full_name')

    Project = serializers.ReadOnlyField(
        source='project.name',
    )
    ObservationType = serializers.ReadOnlyField(
        source='type.name',
    )

    class Meta:
        model = Observation
        geo_field = 'geometry'  # required for this serializer
        exclude = ('parentobs', 'observer', 'type', 'site', 'project')

    # this includes the JSON field into the 'properties' dictionary of the geojson
    def to_representation(self, obj):
        data = super().to_representation(obj)
        kv = data['properties'].pop('kv') or {}
        data['properties'].update(kv)
        return data


class SiteSerializer(GeoFeatureModelSerializer):
    # 'site_observations' is a related name in Observation model 'site' field
    site_observations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Site
        geo_field = "geometry"
        fields = ('id', 'name', 'geometry', 'site_observations')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('site_observations')
        return queryset

    def get_site_observations(self, obj):
        request = self.context['request']
        queryset = obj.site_observations.all()
        if request:
            queryset = filter_site_observations(queryset, request, prefix='')

        return ObsSerializer(queryset, many=True).data


class ProjectSerializer(serializers.ModelSerializer):
    ProjectCoordinator = serializers.ReadOnlyField(
        source='project.project_coordinator.full_name'
    )

    class Meta:
        model = Project
        fields = ('__all__')


class RasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasterLayer
        fields = ('__all__')


class VectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorLayer
        fields = ('__all__')


class MapSerializer(serializers.ModelSerializer):
    rasters = RasterSerializer(required=False, many=True)
    vectors = VectorSerializer(required=False, many=True)

    class Meta:
        model = Map
        # fields = ('name','rasters', 'vectors','center')
        fields = ('__all__')


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'user_location')


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ('id', 'user', 'user_status', 'project')


class AuthUserSerializer(serializers.ModelSerializer):
    user_projects = UserStatusSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'user_location',
                  'default_project', 'user_projects')

    # def get_user_projects(self, obj):
    #     request = self.context['request']
    #     queryset = UserStatus.objects.all()
    #     if request:
    #         queryset = filter(queryset, project_user=request.user)

    #     return UserStatusSerializer(queryset, many=True).data


# NOT USED


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2',
                  'user_location', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

# overwrite save method
    def save(self):
        newuser = CustomUser(
            email=self.validated_data['email'].lower(),
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            user_location=self.validated_data['user_location'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        newuser.set_password(password)  # hashes the pwd
        newuser.save()
        return newuser

# NOT USED


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')
