from django.db import models
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.contrib.auth.models import User
from django_facebook.models import FacebookProfileModel
from django.db.models.signals import post_save
import ast
class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Profile(UserenaBaseProfile, FacebookProfileModel):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='my_profile')
    website = models.URLField(null=True, blank=True)
    zipcode = models.IntegerField(max_length=5, null=True, blank=True)
    genre = ListField()

    def __unicode__(self):
        return self.user.username

    def create_facebook_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_facebook_profile, sender=User)
# Create your models here.

