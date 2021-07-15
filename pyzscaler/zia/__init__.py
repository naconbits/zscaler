import os

from restfly.session import APISession

from pyzscaler.utils import obfuscate_api_key
from pyzscaler.version import version
from .users import UserManagementAPI


class ZIA(APISession):
    """A Controller to access Endpoints in the Zscaler Internet Access (ZIA) API.

     The ZIA object stores the session token and simplifies access to CRUD options within the ZIA platform.

     Attributes:
         api_key (str): The ZIA API key generated from the ZIA console.
         username (str): The ZIA administrator username.
         password (str): The ZIA administrator password.

     """
    _vendor = 'Zscaler'
    _product = 'Zscaler Internet Access'
    _build = version
    _box = True
    _box_attrs = {
        'camel_killer_box': True
    }
    _env_base = 'ZIA'
    _env_cloud = 'zscaler'
    _url = 'https://zsapi.zscaler.net/api/v1'

    def __init__(self, **kw):
        self._api_key = kw.get('api_key',
                               os.getenv(f'{self._env_base}_API_KEY'))
        self._username = kw.get('username',
                                os.getenv(f'{self._env_base}_USERNAME'))
        self._password = kw.get('password',
                                os.getenv(f'{self._env_base}_PASSWORD'))
        self._env_cloud = kw.get('cloud',
                                 os.getenv(f'{self._env_base}_CLOUD'))
        self._url = f'https://zsapi.{self._env_cloud}.net/api/v1'
        super(ZIA, self).__init__(**kw)

    def _build_session(self, **kwargs) -> None:
        """Creates a ZIA API session using the /api/v1/authenticatedSession endpoint.

        :param kwargs:
        :return:
        """
        print(self._url)
        super(ZIA, self)._build_session(**kwargs)
        api_obf = obfuscate_api_key(self._api_key)

        payload = {
            'apiKey': api_obf['key'],
            'username': self._username,
            'password': self._password,
            'timestamp': api_obf['timestamp']
        }
        headers = {
            'Content-Type': 'application/json',
        }
        self.post('authenticatedSession', headers=headers, json=payload)

    @property
    def users(self):
        """
        The interface object for the :ref:`ZIA User Management interface <zia-users>`.

        """
        return UserManagementAPI(self)