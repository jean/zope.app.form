##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: widget.py,v 1.14 2004/03/13 21:37:17 srichter Exp $
"""
import traceback
from warnings import warn
from zope.app import zapi
from zope.app.form.interfaces import IWidget
from zope.component.interfaces import IViewFactory
from zope.interface import implements
from zope.i18n import translate

class Widget(object):
    """Mixin class providing functionality common accross view types."""
    
    implements(IWidget)

    _prefix = 'field.'
    _data_marker = object()
    _data = _data_marker
    
    visible = True

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.name = self._prefix + context.__name__
        
    title = property(lambda self: self._translate(
        self.context.title))
    
    description = property(lambda self: self._translate(
        self.context.description))
    
    def _translate(self, text):
        return translate(self.context, text, "zope",
                         context=self.request, default=text)
            
    def _renderedValueSet(self):
        """Returns True if the the widget's rendered value has been set.
        
        This is a convenience method that widgets can use to check whether
        or not setRenderedValue was called.
        """
        return self._data is not self._data_marker

    def setPrefix(self, prefix):
        if not prefix.endswith("."):
            prefix += '.'
        self._prefix = prefix
        self.name = prefix + self.context.__name__

    def setRenderedValue(self, value):
        self._data = value

class CustomWidgetFactory(object):
    """Custom Widget Factory."""
    implements(IViewFactory)

    def __init__(self, *args, **kw):
        self._widget_factory = args[0]
        if len(args) > 1:
            self.args = args[1:]
        else:
            self.args = ()
        self.kw = kw

    def __call__(self, context, request):
        args = (context, request) + self.args
        instance = self._widget_factory(*args)
        for item in self.kw.items():
            setattr(instance, item[0], item[1])
        return instance
