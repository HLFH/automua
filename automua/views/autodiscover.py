"""
automua™ is a trademark of "Gaspard d'Hautefeuille" and may not be used 
by third parties without the prior written permission of the author.

Copyright © 2022 Gaspard d'Hautefeuille: fix Autodiscover requests
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
from lxml.etree import Element
from lxml.etree import fromstring

from flask import abort
from flask import request
from flask.views import MethodView

from automua import AutoMuaException
from automua import NotFoundException
from automua import log
from automua.generators.outlook import NS_REQUEST
from automua.generators.outlook import OutlookGenerator
from automua.views import EMAIL_OUTLOOK
from automua.views import MailConfig


class OutlookView(MailConfig, MethodView):
    """Autoconfigure mail, Outlook-style."""

    def post(self):
        """Outlook-style POST request is expected to contain XML."""
        if not self.is_expected_content_type():
            message = 'Unexpected content type'
            log.error(message)
            return message, 400
        element: Element = fromstring(request.data)
        ns = element.xpath("namespace-uri()")
        if ns == NS_REQUEST:
            element = element.find(f'n:Request/n:{EMAIL_OUTLOOK}', {'n': ns})
        else: 
            message = 'Invalid XML namespace'
            log.error(message)
            return message, 400
        if element is None:
            message = f'Missing request argument "{EMAIL_OUTLOOK}"'
            log.error(message)
            return message, 400
        try:
            return self.config_from_address(element.text)
        except NotFoundException:
            return '', 204
        except AutoMuaException as e:
            log.exception(e)
            abort(400)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = OutlookGenerator().client_config(local_part, domain_part, realname)
        return data
