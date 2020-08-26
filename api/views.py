from obs.models import Observation, Site, Project, ObservationType
from obs.filters import filter_site_observations
from maps.models import RasterLayer, VectorLayer, Map
from posts.models import Post
from users.models import CustomUser, UserStatus
from rest_framework import viewsets, status, permissions, generics, reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoginSerializer, SiteSerializer, ObsGeoSerializer, ObsSerializer, MapSerializer, ProjectSerializer, UserSerializer, RegistrationSerializer, PostSerializer, UserStatusSerializer, ObservationTypeSerializer, AuthUserSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from .utils import MultipartJsonParser
from rest_framework.views import APIView
from .serializers import FileSerializer
# FILTERS
# from rest_framework import filters
# from rest_framework.filters import SearchFilter, OrderingFilter
# import rest_framework_filters as filters
# from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend
# from django_filters import rest_framework as filters
# import django_filters


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all().order_by(
        'pk').distinct('pk')
    serializer_class = SiteSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = filter_site_observations(
            queryset, self.request, prefix='site_observations')

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


# class FileUploadView(APIView):
#     parser_classes = (FileUploadParser,)

#     def post(self, request, filename, format=None):
#         file_obj = request.FILES['file']
#         # do some stuff with uploaded file
#         return Response(status=204)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # put password reset functions here?
    # permission_classes = (permissions.IsAdminUser,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-pk')
    serializer_class = ProjectSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-pk')
    serializer_class = PostSerializer


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all().order_by('-pk')
    serializer_class = MapSerializer


class AuthUserView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            content = {'message': 'Unauthorized'}
            response = JsonResponse(content, status=401)
            return response

        serializer = AuthUserSerializer(request.user)
        return Response(serializer.data)
        # else:
        #     content = {'message': 'Unauthenticated'}
        #     response = JsonResponse(content, status=401)
        #     return response


class UserStatusViewSet(viewsets.ModelViewSet):
    queryset = UserStatus.objects.all().order_by('-id')
    serializer_class = UserStatusSerializer


class ObsPostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        obs_serializer = ObsSerializer(data=request.data)
        if obs_serializer.is_valid():
            obs_serializer.save()
            return Response(obs_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(obs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObservationViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.all().select_related(
        'site').select_related('observer').select_related('obs_type').select_related('project').order_by('pk')
    serializer_class = ObsGeoSerializer

    # @action(detail=True, methods=['post', 'put'], serializer_class=FileUploadSerializer,
    #parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return ObsSerializer
        return self.serializer_class


class ObservationTypeViewSet(viewsets.ModelViewSet):
    queryset = ObservationType.objects.all().order_by('pk')
    serializer_class = ObservationTypeSerializer


# class MyObsList(generics.ListAPIView):
#     serializer_class = ObsGeoSerializer
#     filter_backends = (SearchFilter, OrderingFilter)
#     search_fields = ('@site__name', 'kv')

#     def get_queryset(self):
#         """
#         This view should return a list of all the observations
#         by the currently authenticated user.
#         """
#         user = self.request.user
#         return Observation.objects.filter(observer=user)


class MyProjectList(generics.ListAPIView):
    serializer_class = ObsGeoSerializer
    # filter_backends = (SearchFilter, OrderingFilter)
    # search_fields = ('@site__name', 'kv')
    queryset = Observation.objects.all()
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ('project', 'observer')
    # def get_queryset(self):
    #     """
    #     This view should return a list of all the project observations
    #     in the currently authenticated user's project.
    #     """
    #     project = 7
    #     return Observation.objects.filter(project=project)


# class ObsFilter(filters.FilterSet):

#     class Meta:
#         model = Observation
#         fields = {'project_id': ['exact']}


# class SiteFilterSet(filters.FilterSet):
#     has_obs = filters.BooleanFilter(
#         field_name='site_observations', lookup_expr='isnull')

#     class Meta:
#         model = Site
#         fields = ('id', 'name', 'no_obs')


# NOT USED
@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':  # this if probably not needed
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            newuser = serializer.save()
            data['response'] = "You have successfully registered as a new user."
            data['email'] = newuser.email
            data['name'] = newuser.first_name + ' ' + newuser.last_name
            data['user_location'] = newuser.user_location
        else:
            data = serializer.errors
        return Response(data)

# from SO post; NOT USED


class Login(APIView):
    # permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email and password:
            user_obj = CustomUser.objects.filter(email__iexact=email)
            if user.exists() and user.first().check_password(password):
                user = LoginSerializer(user_obj)
                data_list = {}
                data_list.update(user.data)
                return Response({"message": "Login Succeeded", "data": data_list, "code": 200})
            else:
                message = "Unable to login with given credentials"
                return Response({"message": message, "code": 500, 'data': {}})
        else:
            message = "Invalid login details."
            return Response({"message": message, "code": 500, 'data': {}})

# here's a class-based login view with the wrong parent model


class LoginView(generics.RetrieveAPIView):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()

    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def _error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'user_id': None,
        }

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_100_OK)
            return self._error_response('disabled')
        return self._error_response('invalid')
