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
$Id: test_textareawidget.py,v 1.1 2004/03/14 01:11:37 srichter Exp $
"""
import unittest, doctest

from zope.app.form.interfaces import IInputWidget
from zope.app.form.browser.widget import TextAreaWidget
from zope.app.form.browser.tests.test_browserwidget import BrowserWidgetTest
from zope.interface.verify import verifyClass

class TextAreaWidgetTest(BrowserWidgetTest):
    """Documents and tests the text area widget.

        >>> verifyClass(IInputWidget, TextAreaWidget)
        True
    """

    _WidgetFactory = TextAreaWidget

    def testProperties(self):
        self.assertEqual(self._widget.tag, 'input')
        self.assertEqual(self._widget.type, 'text')
        self.assertEqual(self._widget.cssClass, '')
        self.assertEqual(self._widget.extra, '')
        self.assertEqual(self._widget.width, 60)
        self.assertEqual(self._widget.height, 15)

    def testRender(self):
        value = "Foo Value"
        self._widget.setRenderedValue(value)
        check_list = ('rows="15"', 'cols="60"', 'id="field.foo"',
                      'name="field.foo"', 'textarea')
        self.verifyResult(self._widget(), check_list)
        check_list = ('style="color: red"',) + check_list
        self._widget.extra = 'style="color: red"'
        self.verifyResult(self._widget(), check_list)
        check_list = ('type="hidden"', 'id="field.foo"', 'name="field.foo"',
                      'value="Foo Value"')
        self.verifyResult(self._widget.hidden(), check_list)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TextAreaWidgetTest),
        doctest.DocTestSuite(),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
