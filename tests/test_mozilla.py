"""
automua™ is a trademark of "Gaspard d'Hautefeuille" and may not be used 
by third parties without the prior written permission of the author.

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
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring

from automua.database import BIGCORP_NAME
from automua.database import EGGS_DOMAIN
from automua.database import EXAMPLE_COM
from automua.database import EXAMPLE_NET
from automua.database import EXAMPLE_ORG
from automua.database import SERVERLESS_DOMAIN
from automua.database import sample_server_names
from automua.server import MOZILLA_CONFIG_ROUTE
from automua.views import CONTENT_TYPE_XML
from tests.base import TestCase
from tests.base import body


class MozillaRoutes(TestCase):
    """Tests for Autoconfig routes."""

    @staticmethod
    def imap_server_elements(element: Element) -> List[Element]:
        return element.findall('emailProvider/incomingServer/[@type="imap"]/hostname')

    @staticmethod
    def pop_server_elements(element: Element) -> List[Element]:
        return element.findall('emailProvider/incomingServer/[@type="pop3"]/hostname')

    @staticmethod
    def smtp_server_elements(element: Element) -> List[Element]:
        return element.findall('emailProvider/outgoingServer/[@type="smtp"]/hostname')

    def test_mozilla_missing_arg(self):
        with self.app:
            r = self.get(MOZILLA_CONFIG_ROUTE)
            self.assertEqual(400, r.status_code)

    def test_mozilla_no_domain_match(self):
        with self.app:
            r = self.get_mozilla_config('a@b.c')
            self.assertEqual(204, r.status_code)

    def test_mozilla_domain_match(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_COM}')
            self.assertEqual(200, r.status_code)
            self.assertEqual(CONTENT_TYPE_XML, r.mimetype)
            e: Element = fromstring(body(r))
            x = e.findall('emailProvider/displayName')
            self.assertEqual(BIGCORP_NAME, x[0].text)

    def test_mozilla_pop(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_ORG}')
            x = self.pop_server_elements(fromstring(body(r)))
            self.assertEqual(sample_server_names['pop1'], x[0].text)

    def test_mozilla_smtp(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EXAMPLE_NET}')
            x = self.smtp_server_elements(fromstring(body(r)))
            self.assertEqual(sample_server_names['smtp1'], x[0].text)

    def test_domain_without_servers(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{SERVERLESS_DOMAIN}')
            b = fromstring(body(r))
            self.assertEqual([], self.imap_server_elements(b))
            self.assertEqual([], self.smtp_server_elements(b))

    def test_invalid_server(self):
        with self.app:
            r = self.get_mozilla_config(f'a@{EGGS_DOMAIN}')
            self.assertEqual(400, r.status_code)


if __name__ == '__main__':
    unittest.main()
