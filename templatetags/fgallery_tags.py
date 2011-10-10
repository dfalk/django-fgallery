#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import Library, Node
from django.utils.translation import ugettext as _

register = Library()

@register.filter
def class_name(value):
    return "%s-%s" % (value.__module__.split('.')[0], value.__class__.__name__.lower())
