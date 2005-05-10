##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""$Id$
"""
import unittest

from zope.interface import Interface, implements
from zope.publisher.browser import TestRequest
from zope.schema import TextLine, accessors
from zope.schema.interfaces import ITextLine
from zope.security.checker import InterfaceChecker, ProxyFactory

from zope.app.testing import ztapi
from zope.app.testing.placelesssetup import PlacelessSetup

from zope.app.form.browser.editwizard import EditWizardView
from zope.app.form.browser import TextWidget
from zope.app.form.interfaces import IInputWidget
from zope.app.location.interfaces import ILocation
from zope.app.form.tests import utils

class I(Interface):
    foo = TextLine(title=u"Foo")
    bar = TextLine(title=u"Bar")
    a   = TextLine(title=u"A")
    b   = TextLine(title=u"B", min_length=0, required=False)
    getbaz, setbaz = accessors(TextLine(title=u"Baz"))

class EV(EditWizardView):
    schema = I
    object_factories = []
    use_session = None

class C(object):
    implements(I)
    __Security_checker__ = utils.SchemaChecker(I)
    foo = u"c foo"
    bar = u"c bar"
    a   = u"c a"
    b   = u"c b"
    _baz = u"c baz"
    def getbaz(self): return self._baz
    def setbaz(self, v): self._baz = v


class IFoo(Interface):
    foo = TextLine(title=u"Foo")

class IBar(Interface):
    bar = TextLine(title=u"Bar")

class Foo(object):
    implements(IFoo)
    __Security_checker__ = utils.SchemaChecker(IFoo)
    foo = u'Foo foo'
    
class ConformFoo(object):
    implements(IFoo)

    foo = u'Foo foo'

    def __conform__(self, interface):
        if interface is IBar:
            return OtherFooBarAdapter(self)

            
class FooBarAdapter(object):
    implements(IBar, ILocation)
    __used_for__ = IFoo
    __Security_checker__ = utils.SchemaChecker(IBar)
    def __init__(self, context):
        self.context = context

    def getbar(self): return self.context.foo
    def setbar(self, v): self.context.foo = v

    bar = property(getbar, setbar)
    
class OtherFooBarAdapter(FooBarAdapter):
    pass

class BarV(EditWizardView):
    schema = IBar
    object_factories = []
    use_session = None

class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        ztapi.browserViewProviding(ITextLine, TextWidget, IInputWidget)
        ztapi.provideAdapter(IFoo, IBar, FooBarAdapter)

    def test_setUpWidget(self):
        c = C()
        request = TestRequest()
        v = EV(c, request)

    def test_setUpWidget_via_adapter(self):
        f = Foo()
        request = TestRequest()
        v = BarV(f, request)

    def test_setUpWidget_via_conform_adapter(self):        
        f = ConformFoo()
        request = TestRequest()
        v = BarV(f, request)
        
def test_suite():
    return unittest.makeSuite(Test)

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')