from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from obs.models import Project
# from .managers import CustomUserManager


class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """user model for this site, following https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username

    Have finally got username out of signup form."""
    username = None
    email = models.EmailField(
        'email address', unique=True, help_text='This will be your login identity but will not be displayed')
    full_name = models.CharField(_('full name'), max_length=60, blank=False, default='',
                                 help_text="Required. Your full name will be your display name.")

    user_location = models.CharField(
        max_length=200, blank=False, help_text="Your location, such as town, county, state, country")
    default_project = models.ForeignKey('obs.Project', null=True, blank=True, default=1,
                                        on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'  # (this is in settings)
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserStatus(models.Model):

    project = models.ForeignKey(
        Project, blank=False, null=False, on_delete=models.CASCADE, related_name='user_project')
    user = models.ForeignKey(
        CustomUser, blank=False, null=False, on_delete=models.CASCADE, related_name='project_user')
    APPRENTICE = 'AP'
    OBSERVER = 'OB'
    COORDINATOR = 'CO'
    USER_STATUS_CHOICES = [
        (APPRENTICE, 'Apprentice'),
        (OBSERVER, 'Observer'),
        (COORDINATOR, 'Coordinator (staff)'),
    ]
    user_status = models.CharField(
        max_length=2, blank=False,
        choices=USER_STATUS_CHOICES,
        default=OBSERVER,
    )

    def __str__(self):
        return '%s has status %s on %s' % (self.user, self.user_status, self.project)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'User statuses'
