from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from utils import get_name


class BaseFeature(models.Model):
    '''
    An abstract base class that any custom feature models should
    subclass.
    '''
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        blank=False,
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=False,
    )

    site = models.ForeignKey(
        Site,
        verbose_name=_('Site'),
        default=Site.objects.get_current,
    )

    class Meta:
        abstract = True


def get_ready_progress():
    return getattr(settings, 'FEATURES_READY_PROGRESS', 100)


class ReadyFeaturesManager(models.Manager):

    def get_query_set(self):
        return super(ReadyFeaturesManager, self).get_query_set().filter(
            progress=get_ready_progress()
        )


class LaunchedFeaturesManager(models.Manager):

    def get_query_set(self):
        return super(LaunchedFeaturesManager, self).get_query_set().filter(
            is_launched=True
        )


class StoppedFeaturesManager(models.Manager):

    def get_query_set(self):
        return super(StoppedFeaturesManager, self).get_query_set().filter(
            is_stopped=True
        )


class Feature(BaseFeature):
    progress = models.IntegerField(
        verbose_name=_('Progress'),
        blank=True,
        default=0,
        help_text=_('In percents'),
    )

    is_launched = models.BooleanField(
        verbose_name=_('Is launched'),
        default=False,
    )
    is_stopped = models.BooleanField(
        verbose_name=_('Is stopped'),
        default=False,
    )

    people = models.ManyToManyField(
        User,
        related_name='features',
        verbose_name=_('People involved'),
    )

    status = models.TextField(
        verbose_name=_('Status'),
        blank=True,
    )

    objects = models.Manager()
    ready = ReadyFeaturesManager()
    launched = LaunchedFeaturesManager()
    stopped = StoppedFeaturesManager()

    def __unicode__(self):
        return self.title

    @property
    def is_ready(self):
        return self.progress == get_ready_progress()

    def get_names(self):
        return map(get_name, self.people.all())
