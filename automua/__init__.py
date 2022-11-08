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
import logging

IDENTIFIER = "automua" # Do not change this!
VERSION = '2022.6.6'

PLACEHOLDER_ADDRESS = r'%EMAILADDRESS%'
PLACEHOLDER_DOMAIN = r'%EMAILDOMAIN%'
PLACEHOLDER_LOCALPART = r'%EMAILLOCALPART%'


class AutoMuaException(Exception):
    """Exception base class for this application.

    Will result in HTTP code 400 (bad request).
    """
    pass


class NotFoundException(AutoMuaException):
    """Exception base class for lookup failures etc.

    Will result in HTTP code 204 (no content).
    """
    pass


class InvalidEMailAddressError(AutoMuaException):
    """Email address is invalid/unparseable."""
    pass


class DomainNotFound(NotFoundException):
    """Database did not contain the given domain."""
    pass


class NoProviderForDomain(AutoMuaException):
    """Database did not contain a provider for the given address."""
    pass


class NoServersForDomain(AutoMuaException):
    """Database did not contain any servers for the given address."""
    pass


class InvalidServerType(AutoMuaException):
    """Database contains an invalid server type."""
    pass


class InvalidAuthenticationType(AutoMuaException):
    """Database contains an invalid authentication type."""
    pass


class LdapLookupError(AutoMuaException):
    """LDAP lookup failed."""
    pass


class LdapNoMatch(NotFoundException):
    """LDAP lookup returned no match."""
    pass


log = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter())
log.addHandler(_handler)
log.setLevel(logging.DEBUG)
log.warning(f'Running {IDENTIFIER} version {VERSION}')
