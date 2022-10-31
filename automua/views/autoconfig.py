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
from flask import abort
from flask import request
from flask.views import MethodView

from automua import AutoMuaException
from automua import NotFoundException
from automua import log
from automua.generators.mozilla import MozillaGenerator
from automua.views import EMAIL_MOZILLA
from automua.views import MailConfig


class MozillaView(MailConfig, MethodView):
    """Autoconfigure mail, Mozilla-style."""

    def get(self):
        """GET request is expected to contain ?emailaddress=user@example.com"""
        address = request.args.get(EMAIL_MOZILLA, '')
        if not address:
            message = f'Missing request argument "{EMAIL_MOZILLA}"'
            log.error(message)
            return message, 400
        try:
            return self.config_from_address(address)
        except NotFoundException:
            return '', 204
        except AutoMuaException as e:
            log.exception(e)
            abort(400)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = MozillaGenerator().client_config(local_part, domain_part, realname)
        return data
