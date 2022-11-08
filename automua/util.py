"""
automua™ is a trademark of "Gaspard d'Hautefeuille" and may not be used 
by third parties without the prior written permission of the author.

Copyright © 2022 Gaspard d'Hautefeuille: replace SSL by TLS
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
import os
import re
from uuid import uuid4

from automua import InvalidEMailAddressError
from automua import PLACEHOLDER_ADDRESS
from automua import PLACEHOLDER_DOMAIN
from automua import PLACEHOLDER_LOCALPART
from automua import log

email_address_re = re.compile(r'^([^@]+)@([^@]+)$', re.IGNORECASE)


def from_dict(data: dict, key: str, default: object = None):
    if key in data:
        return data[key]
    return default


def from_environ(env_var_name: str, default: object = None):
    if env_var_name in os.environ:
        return os.environ[env_var_name]
    return default


def parse_email_address(address: str):
    if address:
        match = email_address_re.search(address)
        if match:
            return match[1], match[2]
    raise InvalidEMailAddressError('Invalid email address')


def unique() -> str:
    return uuid4().hex


def expand_placeholders(string: str, local_part: str, domain_part: str) -> str:
    if not string:
        return ''
    placeholder_map = {
        PLACEHOLDER_ADDRESS: f'{local_part}@{domain_part}',
        PLACEHOLDER_DOMAIN: domain_part,
        PLACEHOLDER_LOCALPART: local_part,
    }
    for k, v in placeholder_map.items():
        string = string.replace(k, v)
    return string


def socket_type_needs_tls(socket_type: str):
    """Map socket type to True (use TLS) or False (do not use TLS)."""
    if 'SSL' == socket_type:
        return True
    elif 'TLS' == socket_type:
        return True
    elif 'STARTTLS' != socket_type:
        """
        Existing versions of automua return False for socket types other than
        SSL, TLS and STARTTLS. This can cause unexpected results. Future automua versions
        will raise an exception for invalid socket types, so log an error to notify
        users of this upcoming change.
        """
        log.error(f'Unexpected socket type "{socket_type}" will cause a failure in future versions')
    return False


def strip_none_values(data: dict) -> dict:
    """Return copy of a dict containing only keys without 'None' values."""
    return {k: v for (k, v) in data.items() if v is not None}
