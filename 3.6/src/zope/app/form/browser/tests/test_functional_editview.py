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
"""Editview tests

$Id$
"""
import unittest
import transaction
from persistent import Persistent

import zope.security.checker
from zope.interface import Interface, implements
from zope.schema import TextLine
from zope.traversing.api import traverse

from zope.app.form.browser.editview import EditView
from zope.app.form.testing import AppFormLayer
from zope.app.form.browser.tests.support import *
from zope.app.testing.functional import BrowserTestCase

class IFoo(Interface):

    optional_text = TextLine(required=False)
    required_text = TextLine(required=True)

class Foo(Persistent):

    implements(IFoo)

class Test(BrowserTestCase):

    def setUp(self):
        BrowserTestCase.setUp(self)
        registerEditForm(IFoo)
        defineSecurity(Foo, IFoo)

    def test_rollback_on_error(self):
        """Tests rollback when a widget error occurs.

        When one or more errors are generated by input widgets, the current
        transaction should be rolledback to ensure object integrity.
        """
        self.getRootFolder()['foo'] = Foo()
        self.getRootFolder()['foo'].required_text = u'initial required'
        self.getRootFolder()['foo'].optional_text = u'initial optional'
        transaction.commit()

        # submit form with legal value for optional_text and invalid for
        # required_text
        old_update = EditView.update
        try:
            def new_update(self):
                # This update changes something after form validation has failed.
                # Side effects like this should not be committed.
                # http://www.zope.org/Collectors/Zope3-dev/655
                result = old_update(self)
                self.context.required_text = u'changed after form validation'
                return result
            EditView.update = new_update
            response = self.publish('/foo/edit.html', form={
                'field.optional_text': u'',
                'field.required_text': u'',
                'UPDATE_SUBMIT': ''})
            self.assertEqual(response.getStatus(), 200)
        finally:
            EditView.update = old_update

        # confirm that one errors exists
        self.assert_(patternExists(
            'There are <strong>1</strong> input errors.', response.getBody()))

        # confirm that foo was not modified
        foo = traverse(self.getRootFolder(), 'foo')
        self.assertEquals(foo.required_text, u'initial required')
        self.assertEquals(foo.optional_text, u'initial optional')


def test_suite():
    suite = unittest.TestSuite()
    Test.layer = AppFormLayer
    suite.addTest(unittest.makeSuite(Test))
    return suite

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')


