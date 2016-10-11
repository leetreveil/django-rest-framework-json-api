# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class BaseModel(models.Model):
    """
    I hear RoR has this by default, who doesn't need these two fields!
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Blog(BaseModel):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Author(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AuthorBio(BaseModel):
    author = models.OneToOneField(Author, related_name='bio')
    body = models.TextField()

    def __str__(self):
        return self.author.name


@python_2_unicode_compatible
class Entry(BaseModel):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField(null=True)
    pub_date = models.DateField(null=True)
    mod_date = models.DateField(null=True)
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline


@python_2_unicode_compatible
class Comment(BaseModel):
    entry = models.ForeignKey(Entry)
    body = models.TextField()
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.body


class Target(models.Model):
    '''
    The connection's targeting information
    '''
    # references to Audience.id's in the audience_service.
    audience_id = models.IntegerField(help_text='The ID of the audience we are profiling')
    base_audience_id = models.IntegerField(help_text='The ID of the base audience for the profile')

    brand_id = models.IntegerField(help_text='brand ID', db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    creator = models.IntegerField(null=True, help_text='bouncer user ID')
    name = models.CharField(max_length=191, null=True, db_index=True)

    # Optimizations
    instagram_placement = models.BooleanField(default=False, db_index=True)
    latest_profile = models.ForeignKey('Profile', related_name='+', null=True,
                                       help_text='The most recently created related Profile')


class FacebookAdTargetingCategory(models.Model):
    '''
    Categories that we profile overlaps for in the Audience Profiler.
    '''
    audience_type = models.CharField(max_length=128, db_index=True)
    platform_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128, db_index=True)
    description = models.CharField(max_length=256, null=True)
    path = models.CharField(max_length=256, null=True)
    last_updated = models.DateField(auto_now=True)


class Profile(models.Model):
    '''
    An instance of an audience profile being run.
    This model represents what we generally mean when we say "run me an audience profile." It is
    required to group a set of ``ProfileDatum``s as one profile/report.
    '''
    created = models.DateTimeField(auto_now_add=True)
    audience_reach = models.IntegerField()
    base_audience_reach = models.IntegerField()
    bias_normalizer = models.BooleanField(default=False,
                                          help_text="Use this record to normalize interest biases")
    target = models.ForeignKey(Target)


class ProfileDatum(models.Model):
    '''
    Profile Datums for Targeting Data
    '''
    biased_index = models.FloatField(null=False, db_index=True)
    unbiased_index = models.FloatField(null=True, db_index=True)
    opportunity_score = models.FloatField(db_index=True)
    reach_audience = models.IntegerField()
    reach_base = models.IntegerField()
    created_time = models.DateTimeField(auto_now=True, db_index=True)
    category = models.ForeignKey(FacebookAdTargetingCategory)
    # profile = models.ForeignKey(Profile)
