##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Browser widgets for text-like data

$Id: objectwidget.py,v 1.1 2004/03/17 17:35:02 philikon Exp $
"""
from zope.interface import implements
from zope.schema import getFieldNamesInOrder

from zope.app.form.interfaces import IInputWidget
from zope.app.form.browser.widget import BrowserWidget
from zope.app.form.utility import setUpEditWidgets, applyWidgetsChanges

class ObjectWidget(BrowserWidget):
    """A widget over an Interface that contains Fields.

    "factory"  - factory used to create content that this widget (field)
                 represents
    *_widget   - Optional CustomWidgets used to generate widgets for the
                 fields in this widget
    """

    implements(IInputWidget)
    
    _object = None      # the object value (from setRenderedValue & request)
    _request_parsed = False

    def __init__(self, context, request, factory, **kw):
        super(ObjectWidget, self).__init__(context, request)

        # factory used to create content that this widget (field)
        # represents
        self.factory = factory

        # handle foo_widget specs being passed in
        self.names = getFieldNamesInOrder(self.context.schema)
        for k, v in kw.items():
            if k.endswith('_widget'):
                setattr(self, k, v)

        # set up my subwidgets
        self._setUpEditWidgets()

    def setPrefix(self, prefix):
        super(ObjectWidget, self).setPrefix(prefix)
        self._setUpEditWidgets()

    def _setUpEditWidgets(self):
        # subwidgets need a new name
        setUpEditWidgets(self, self.context.schema, source=self.context,
                         prefix=self.name, names=self.names, 
                         context=self.context)

    def __call__(self):
        """Render the widget
        """
        render = []

        # XXX see if there's some widget layout already

        # generate each widget from fields in the schema
        field = self.context
        title = field.title or field.__name__
        render.append('<fieldset><legend>%s</legend>'%title)
        for name, widget in self.getSubWidgets():
            render.append(widget.row())
        render.append('</fieldset>')

        return '\n'.join(render)

    def getSubWidgets(self):
        l = []
        for name in self.names:
            l.append((name, getattr(self, '%s_widget'%name)))
        return l

    def hidden(self):
        ''' Render the list as hidden fields '''
        for name, widget in self.getSubWidgets():
            s += widget.hidden()
        return s

    def getInputValue(self):
        """Return converted and validated widget data.

        The value for this field will be represented as an ObjectStorage
        instance which holds the subfield values as attributes. It will
        need to be converted by higher-level code into some more useful
        object (note that the default EditView calls applyChanges, which
        does this).
        """
        content = self.factory()
        for name, widget in self.getSubWidgets():
            setattr(content, name, widget.getInputValue())
        return content

    def applyChanges(self, content):
        field = self.context

        # create our new object value
        value = field.query(content, None)
        if value is None:
            # XXX ObjectCreatedEvent here would be nice
            value = self.factory()

        # apply sub changes, see if there *are* any changes
        # XXX ObjectModifiedEvent here would be nice
        changes = applyWidgetsChanges(self, field.schema, target=value,
                                      names=self.names)

        # if there's changes, then store the new value on the content
        if changes:
            field.set(content, value)

        return changes

    def hasInput(self):
        """Is there input data for the field

        Return True if there is data and False otherwise.
        """
        for name, widget in self.getSubWidgets():
            if widget.hasInput():
                return True
        return False

    def setRenderedValue(self, value):
        """Set the default data for the widget.

        The given value should be used even if the user has entered
        data.
        """
        # re-call setupwidgets with the content
        self._setUpEditWidgets()
        for name, widget in self.getSubWidgets():
            widget.setRenderedValue(getattr(value, name, None))
            
