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
$Id: test_setprefix.py,v 1.1 2004/03/14 01:11:37 srichter Exp $
"""
import unittest

from zope.app.form.browser.widget import TextWidget
from zope.publisher.browser import TestRequest
from zope.schema import Text

class Test(unittest.TestCase):

    def setUp(self):
        field = Text(__name__ = 'foo')
        request = TestRequest()
        request.form['spam.foo'] = u'Foo Value'
        self._widget = TextWidget(field, request)
        self._widget.setPrefix('spam')

    def testGetData(self):
        self.assertEqual(self._widget.getInputValue(), u'Foo Value')

    def testRender(self):
        value = 'Foo Value 2'
        check_list = ('type="text"', 'id="spam.foo"', 'name="spam.foo"',
                      'value="Foo Value 2"', 'size="20"')
        self._widget.setRenderedValue(value)
        self._verifyResult(self._widget(), check_list)
        check_list = ('type="hidden"',) + check_list[1:-1]
        self._verifyResult(self._widget.hidden(), check_list)
        check_list = ('style="color: red"',) + check_list
        self._widget.extra = 'style="color: red"'
        self._verifyResult(self._widget.hidden(), check_list)

    def _verifyResult(self, result, check_list):
        for check in check_list:
            self.assertNotEqual(-1, result.find(check),
                                '"'+check+'" not found in "'+result+'"')



def test_suite():
    return unittest.makeSuite(Test)

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
