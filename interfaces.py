##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Validation Exceptions

$Id$
"""
from zope.schema.interfaces import ValidationError
from zope.component.interfaces import IView
from zope.interface import Attribute, Interface, implements
from zope.schema import Bool
from zope.app.exception.interfaces import UserError

class IWidgetInputError(Interface):
    """Placeholder for a snippet View"""

class WidgetInputError(UserError):
    """One or more user input errors occurred."""
    
    implements(IWidgetInputError)

    def __init__(self, field_name, widget_title, errors):
        """Initialize Error

        'errors' is a ValidationError or a list of ValidationError objects
        """
        UserError.__init__(self, field_name, widget_title, errors)
        self.field_name = field_name
        self.widget_title = widget_title
        self.errors = errors

class MissingInputError(WidgetInputError):
    """Required data was not supplied."""

class ConversionError(WidgetInputError):
    """A conversion error occurred."""

    def __init__(self, error_name, original_exception=None):
        Exception.__init__(self, error_name, original_exception)
        self.error_name = error_name
        self.original_exception = original_exception

InputErrors = WidgetInputError, ValidationError


class ErrorContainer(Exception):
    """A base error class for collecting multiple errors."""

    def append(self, error):
        self.args += (error, )

    def __len__(self):
        return len(self.args)

    def __iter__(self):
        return iter(self.args)

    def __getitem__(self, i):
        return self.args[i]

    def __str__(self):
        return "\n".join(
            ["%s: %s" % (error.__class__.__name__, error)
             for error in self.args]
            )

    __repr__ = __str__

class WidgetsError(ErrorContainer):
    """A collection of errors from widget processing.
    
    widgetValues is a map containing the list of values that were obtained
    from the widget, keyed by field name.
    """
    
    def __init__(self, errors, widgetsData={}):
        Exception.__init__(self, *errors)
        self.widgetsData = widgetsData

class IWidget(IView):
    """Generically describes the behavior of a widget.

    Note that this level must be still presentation independent.
    """

    name = Attribute(
        """The uniquewidget name

        This must be unique within a set of widgets.""")

    label = Attribute(
        """The widget label.
        
        Label may be translated for the request.""")

    hint = Attribute(
        """A hint regarding the use of the widget.
        
        Hints are traditionally rendered using tooltips in GUIs, but may be
        rendered differently depending on the UI implementation.
        
        Hint may be translated for the request.""")
        
    visible = Attribute(
        """A flag indicating whether or not the widget is visible.""")
       
    def setRenderedValue(value):
        """Set the value to be rendered by the widget.

        Calling this method will override any values provided by the user.
        """
        
    def setPrefix(prefix):
        """Set the name prefix used for the widget

        The widget name is used to identify the widget's data within
        input data. For example, for HTTP forms, the widget name is
        used for the form key.
        """

class IInputWidget(IWidget):
    """A widget for editing a field value."""

    required = Bool(
        title=u"Required",
        description=u"""If True, widget should be displayed as requiring input.
        
        By default, this value is the field's 'required' attribute. This
        field can be set to False for widgets that always provide input (e.g.
        a checkbox) to avoid unnecessary 'required' UI notations.
        """)

    def validate():
        """Validate the widget data.

        If there is no user input and the field is required, then a
        MissingInputError will be raised.

        If there is no user input and the field is not required, then
        the field default value will be returned.

        A WidgetInputError is returned in the case of one or more
        errors encountered, inputting, converting, or validating the data.
        """

    def getInputValue():
        """Return value suitable for the widget's field.

        The widget must return a value that can be legally assigned to
        its bound field or otherwise raise WidgetInputError.

        See validate() for validation performed.
        """

    def applyChanges(content):
        """Validate the widget data and apply it to the content.

        See validate() for validation performed.
        """

    def hasInput():
        """Returns True if the widget has input.

        Input is used by the widget to calculate an 'input value', which is
        a value that can be legally assigned to a field.

        Note that the widget may return True, indicating it has input, but
        still be unable to return a value from getInputValue. Use
        hasValidInput to determine whether or not getInputValue will return
        a valid value.

        A widget that does not have input should generally not be used to
        update its bound field.
        """

    def hasValidInput():
        """Returns True is the widget has valid input.

        This method is similar to hasInput but it also confirms that the
        input provided by the user can be converted to a valid field value
        based on the field constraints.
        """

class IDisplayWidget(IWidget):
    """A widget for displaying a field value."""
