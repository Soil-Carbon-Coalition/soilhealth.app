from obs.models import Site, Observation, Project, ObservationType
from obs.filters import filter_site_observations
from maps.models import Map, RasterLayer, VectorLayer
from users.models import CustomUser, UserStatus
from posts.models import Post
from upload.models import File
from rest_framework import serializers
from django.db.models.functions import Length
# this one formats as geojson:
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage

# used in atlasbiowork obs serializer
from html_json_forms import parse_json_form
import json


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

        if 'crs' in value and value['crs'].get('obs_type', None) == 'name':
            name = value['crs']['properties']['name']
            if name.startswith('urn:ogc:def:crs:EPSG::'):
                geom.srid = int(name.replace('urn:ogc:def:crs:EPSG::', ''))

        if geom.srid is None:
            geom.srid = 4326
        if geom.srid != srid:
            geom.transform(srid)
        return geom


class ObsSerializer(serializers.ModelSerializer):
    '''
    to post data to this serializer, use a FormData object, and append
    fields without any nesting. All fields not in the fixed_fields set 
    will be nested under the kv JSON field, including the file uploads 

    '''
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.__str__()

    class Meta:
        model = Observation
        fields = ('id', 'label', 'project',
                  'obs_type', 'observer', 'site', 'kv')

    def to_internal_value(self, data):
        # Save files and return paths
        for key, value in data.items():
            if isinstance(value, UploadedFile):
                path = 'obs/' + data['project'] + '/' + value.name
                data[key] = default_storage.save(path, value)

        # Convert nested keys to JSON structure
        data = parse_json_form(data)
        fixed_fields = ['observer', 'site', 'project', 'obs_type', 'kv']

        # Extract JSON data into 'kv' field, leaving relational and
        # built-in fields in place.
        data.setdefault('kv', {})
        for key in list(data.keys()):
            if key not in fixed_fields:
                data['kv'][key] = data.pop(key)

        return super().to_internal_value(data)


# THIS ONE YIELDS GEOJSON. USE FOR GET but not POST


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
        source='obs_type.name',
    )

    class Meta:
        model = Observation
        geo_field = 'geometry'  # required for this serializer
        exclude = ('observer', 'obs_type', 'site', 'project')

    # this includes the JSON field into the 'properties' dictionary of the geojson
    def to_representation(self, obj):
        data = super().to_representation(obj)
        kv = data['properties'].pop('kv') or {}
        data['properties'].update(kv)
        return data


class SitePostSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Site
        geo_field = "geometry"
        fields = ('__all__')


class SiteSerializer(GeoFeatureModelSerializer):
    '''
    'site_observations' is a related name in Observation model 'site' field
    This serializer is adapted for searching the nested site_observations array and returning
    geojson features for sites with observations matching the search terms.
    '''
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


class ObsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObservationType
        fields = ('id', 'name', 'slug', 'icon', 'description')


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


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.full_name')
    project = serializers.ReadOnlyField(source='project.name')
    label = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.entered.date()

    def get_label(self, obj):
        return obj.__str__()

    class Meta:
        model = Post
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'user_location')


class UserStatusSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.full_name')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = UserStatus
        fields = ('id', 'user', 'user_name',
                  'user_status', 'project', 'project_name')


class ProjectSerializer(serializers.ModelSerializer):
    observations = serializers.IntegerField()
    posts = serializers.IntegerField()
    obs_types = ObsTypeSerializer(required=False, many=True)
    user = UserStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('__all__')


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


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')


class CurrentUserDefault(serializers.CurrentUserDefault):
    def __call__(self):
        user = super().__call__()
        return user.pk


# class ObservationTypeSerializer(serializers.ModelSerializer):
#     author_id = serializers.HiddenField(
#         default=CurrentUserDefault()
#     )
#     icon = serializers.ImageField(
#         required=False,
#     )

#     class Meta:
#         model = ObservationType
#         fields = ('__all__')
