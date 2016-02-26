# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    """
        A logged user.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='User name in the system')
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

class Deck(models.Model):
    """
        An arbitrary list of words (cards).
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, blank=False)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    """
        A label attached to a card.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=False)
    user = models.ForeignKey(User, blank=False)

    def __unicode__(self):
        return self.name

class Card(models.Model):
    """
        A word in a deck.
    """
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=256, blank=False)
    reading = models.CharField(max_length=256)
    definition = models.CharField(max_length=1024)
    example = models.CharField(max_length=1024)
    deck = models.ForeignKey(Deck, blank=False)
    added = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.word

##class TaggedCard(db.Model):
##    card = db.ReferenceProperty(Card, required=True)
##    tag = db.ReferenceProperty(Tag, required=True)
