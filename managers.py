#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Manager
import datetime

class PublicManager(Manager):
    """Returns published photos that are not in the future."""

    def published(self):
        return self.get_query_set().filter(is_published=True, publish__lte=datetime.datetime.now())
