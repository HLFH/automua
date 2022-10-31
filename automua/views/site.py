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
from flask import url_for
from flask.views import MethodView
from sqlalchemy.exc import OperationalError

from automua import log
from automua.database import EXAMPLE_COM
from automua.model import Provider
from automua.views import EMAIL_MOZILLA


class SiteRoot(MethodView):
    """The site's root page."""

    # noinspection PyMethodMayBeStatic
    def get(self):
        try:
            Provider.query.count()
        except OperationalError as e:
            log.error(e)
            url = url_for('initdb')
            return f'Operational error. Did you remember to <a href="{url}">initialise</a> the database?'
        address = f'abc@{EXAMPLE_COM}'
        url = f'{url_for("mozilla")}?{EMAIL_MOZILLA}={address}'
        return f'<html><body>Show Thunderbird-style <a href="{url}">XML configuration</a> for {address}.</body></html>'
