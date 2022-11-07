"""
automua™ is a trademark of "Gaspard d'Hautefeuille" and may not be used 
by third parties without the prior written permission of the author.

Copyright © 2022 Gaspard d'Hautefeuille: set lxml, XMLSyntaxError, test_invalid_namespace
Copyright © 2019-2022 Ralph Seichter

This file is part of automua.

automua is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

automua is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with automua. If not, see <https://www.gnu.org/licenses/>.
"""
import unittest
from typing import List
from lxml.etree import Element
from lxml.etree import XMLSyntaxError
from lxml.etree import fromstring

from automua.generators.outlook import NS_RESPONSE_PAYLOAD
from automua.database import EGGS_DOMAIN
from automua.database import EXAMPLE_COM
from automua.database import EXAMPLE_NET
from automua.database import EXAMPLE_ORG
from automua.database import SERVERLESS_DOMAIN
from automua.database import sample_server_names
from automua.server import MSOFT_ALTERNATE_ROUTE
from automua.server import MSOFT_CONFIG_ROUTE
from automua.views import CONTENT_TYPE_XML
from automua.views import EMAIL_OUTLOOK
from tests.base import TestCase
from tests.base import body


class MsRoutes(TestCase):
    """Tests for Autodiscover routes."""

    @staticmethod
    def server_elements(element: Element, server_type: str) -> List[Element]:
        ns = {'n': NS_RESPONSE_PAYLOAD}
        r = []
        for p in element.findall('n:Response/n:Account/n:Protocol', ns):
            if p.find('n:Type', ns).text == server_type:
                r.append(p.find('n:Server', ns))
        return r

    def imap_server_elements(self, element: Element) -> List[Element]:
        return self.server_elements(element, 'IMAP')

    def pop_server_elements(self, element: Element) -> List[Element]:
        return self.server_elements(element, 'POP3')

    def smtp_server_elements(self, element: Element) -> List[Element]:
        return self.server_elements(element, 'SMTP')

    def test_ms_empty_post(self):
        with self.app:
            with self.assertRaises(XMLSyntaxError):
                self.post(MSOFT_CONFIG_ROUTE, data=None, content_type=CONTENT_TYPE_XML)

    def test_ms_partial_post(self):
        with self.app:
            self.post(MSOFT_CONFIG_ROUTE, data='<ham/>', content_type=CONTENT_TYPE_XML)
    
    def test_invalid_namespace(self):
        with self.app:
            address = f'a@{EXAMPLE_NET}'
            data = (
                f'<Autodiscover xmlns="myinvalidnamespace">'
                f'<AcceptableResponseSchema>{NS_RESPONSE_PAYLOAD}</AcceptableResponseSchema>'
                '<Request>'
                f'<{EMAIL_OUTLOOK}>{address}</{EMAIL_OUTLOOK}>'
                '</Request>'
                '</Autodiscover>'
            )
            r = self.post(MSOFT_CONFIG_ROUTE, data=data, content_type=CONTENT_TYPE_XML)
            self.assertEqual(400, r.status_code)
            response = list(r.response)
            self.assertEqual(response[0].decode('utf-8', 'strict'), 'Invalid XML namespace')

    def test_ms_no_content_type(self):
        with self.app:
            r = self.post(MSOFT_CONFIG_ROUTE, data='eggs')
            self.assertEqual(400, r.status_code)

    def test_ms_no_domain_match(self):
        with self.app:
            r = self.get_msoft_config('a@b.c')
            self.assertEqual(204, r.status_code)

    def test_ms_valid_domain(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_XML, r.mimetype)
            e: Element = fromstring(body(r))
            self.assertNotEqual([], self.imap_server_elements(e))
            self.assertNotEqual([], self.smtp_server_elements(e))

    def test_ms_pop(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EXAMPLE_ORG}', MSOFT_ALTERNATE_ROUTE)
            x = self.pop_server_elements(fromstring(body(r)))
            self.assertEqual(sample_server_names['pop1'], x[0].text)

    def test_ms_smtp(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_server_elements(fromstring(body(r)))
            self.assertEqual(sample_server_names['smtp1'], x[0].text)

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_msoft_config(f'a@{SERVERLESS_DOMAIN}', MSOFT_ALTERNATE_ROUTE)
            b = fromstring(body(r))
            self.assertEqual([], self.imap_server_elements(b))
            self.assertEqual([], self.smtp_server_elements(b))

    def test_invalid_server(self):
        with self.app:
            r = self.get_msoft_config(f'a@{EGGS_DOMAIN}')
            self.assertEqual(400, r.status_code)


if __name__ == '__main__':
    unittest.main()
