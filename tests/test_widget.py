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
"""Generic Widget Tests

$Id: test_widget.py,v 1.11 2004/05/11 11:17:36 garrett Exp $
"""
from unittest import TestSuite, main, makeSuite
from zope.testing.doctestunit import DocTestSuite

from zope.interface.verify import verifyClass, verifyObject
from zope.component.interfaces import IViewFactory
from zope.publisher.browser import TestRequest
from zope.schema import Text

from zope.app.form import Widget, CustomWidgetFactory
from zope.app.form.interfaces import IWidget
from zope.app.tests.placelesssetup import setUp, tearDown

class TestContext:
    __name__ = 'Test'
    title = 'My Test Context'
    description = 'A test context.'

class FooWidget(Widget):
    pass

context = TestContext()
request = TestRequest()

class TestWidget:
    """Tests basic widget characteristics.

    Widget implements IWidget:

        >>> verifyClass(IWidget, Widget)
        True
        >>> widget = Widget(context, request)
        >>> verifyObject(IWidget, widget)
        True

    The default values for widget are:

        >>> widget.name
        'field.Test'
        >>> widget.label
        'My Test Context'
        >>> widget.hint
        'A test context.'
        >>> widget.visible
        True

    In the last example, the widget name consists of a prefix, a dot, and the
    field name. You can change the prefix used by the widget as follows:

        >>> widget.setPrefix('newprefix')
        >>> widget.name
        'newprefix.Test'

    To configure a widget, call setRenderedValue with a value that the
    widget should display:

        >>> widget.setRenderedValue('Render Me')

    The way a widget renders a value depends on the type of widget. E.g. a
    browser widget will render the specified value in HTML.
    """

class TestInputWidget:
    """Tests the input widget mixin.

    InputWidget is a simple mixin that provides default implementations for
    some of the IInputWidget methods. Because the implementation of widgets
    across UI frameworks is so different, most of the input widget methods
    must be handled by UI specific classes.

    To test the default methods, we must create a basic input widget
    that provides a getInputValue method:

        >>> from zope.app.form import InputWidget
        >>> from zope.app.form.interfaces import WidgetInputError
        >>> class TestInputWidget(InputWidget):
        ... 	def getInputValue(self):
        ...			if self.context.required:
        ...				raise WidgetInputError('', '', None)
        ...			else:
        ...				return 'Foo Bar'

    All widgets rely on a field and a request:

        >>> from zope.schema import Field
        >>> from zope.component.tests.request import Request
        >>> field = Field()
        >>> from zope.interface import Interface
        >>> class ITestRequest(Interface):
        ... 	pass
        >>> widget = TestInputWidget(field, Request(ITestRequest))

    The default implementation of hasValidInput and validate both rely on
    getInputValue to perform the validation of the current widget input.
    In this simple example, the widget will always raise an error when its
    field is read only:

        >>> field.readonly = True
        >>> widget.getInputValue()
        Traceback (most recent call last):
        WidgetInputError: ('', '', None)
        
    A call to validate, however, accomplishes the same thing with improved
    readability:

        >>> widget.validate()
        Traceback (most recent call last):
        WidgetInputError: ('', '', None)

    A call to hasValidInput returns False instead of raising an error:

        >>> widget.hasValidInput()
        False

    By changing the field's required attribute, getInputValue returns a
    simple string:

        >>> field.required = False
        >>> widget.getInputValue()
        'Foo Bar'

    Corredpondingly, validate does not raise an error:

        >>> widget.validate()

    and hasValidInput returns True:

        >>> widget.hasValidInput()
        True
    """

class TestCustomWidgetFactory:
    """Tests the custom widget factory.

    Custom widgets can be created using a custom widget factory. Factories
    are used to assign attribute values to widgets they create:

        >>> factory = CustomWidgetFactory(FooWidget, bar='baz')
        >>> widget = factory(context, request)
        >>> isinstance(widget, FooWidget)
        True
        >>> widget.bar
        'baz'
    """

def test_suite():
    return TestSuite((
        DocTestSuite(setUp=setUp, tearDown=tearDown),
        ))

if __name__=='__main__':
    main(defaultTest='test_suite')
