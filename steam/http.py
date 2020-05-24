# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2020 James

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import json
import logging
import re
from base64 import b64encode
from sys import version_info
from time import time
from typing import TYPE_CHECKING, Union, Awaitable, Tuple, List, Optional, Any

import aiohttp
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey.RSA import construct
from yarl import URL as _URL

from . import __version__, errors
from .models import URL
from .user import ClientUser

if TYPE_CHECKING:
    from Cryptodome.PublicKey.RSA import RsaKey

    from .client import Client
    from .image import Image

log = logging.getLogger(__name__)


async def json_or_text(r: aiohttp.ClientResponse) -> Optional[Union[dict, str]]:
    text = await r.text()
    try:
        if 'application/json' in r.headers['content-type']:  # thanks steam very cool
            return json.loads(text)
    except KeyError:  # this should only really happen if steam is down
        pass
    return text


class Route:
    """Used for formatting API request URLs"""

    def __init__(self, api: str, call: str, version: str = 'v1'):
        self.url = _URL(f'{URL.API}/{api}/{call}/{version}')

    def __str__(self):
        return str(self.url)


class HTTPClient:
    """The HTTP Client that interacts with the Steam web API."""

    SUCCESS_LOG = '{method} {url} has received {text}'
    REQUEST_LOG = '{method} {url} with {payload}{params}has returned {status}'

    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 session: aiohttp.ClientSession,
                 client: 'Client'):
        self._loop = loop
        self._session = session
        self._client = client
        self._state = None
        self._lock = asyncio.Lock()

        self.username = None
        self.password = None
        self.api_key = None
        self.shared_secret = None
        self._one_time_code = None

        self.session_id = None
        self.user = None
        self.logged_in = False
        self._steam_id = None
        self.user_agent = f'steam.py/{__version__} client (https://github.com/Gobot1234/steam.py), ' \
                          f'Python/{version_info[0]}.{version_info[1]}, aiohttp/{aiohttp.__version__}'

    def recreate(self) -> None:
        if self._session.closed:
            self._session = aiohttp.ClientSession(loop=self._loop)

    async def request(self, method: str, url: Union[Route, str],
                      **kwargs) -> Optional[Any]:  # adapted from d.py
        kwargs['headers'] = {
            "User-Agent": self.user_agent,
            **kwargs.get('headers', {})
        }

        async with self._lock:
            for tries in range(5):
                async with self._session.request(method, str(url), **kwargs) as r:
                    payload = kwargs.get('json')
                    params = kwargs.get('params')
                    log.debug(self.REQUEST_LOG.format(
                        method=method,
                        url=url,
                        connective='with' if payload is not None or params is not None else '',
                        payload=f'\nPAYLOAD: {payload}\n' if payload else '',
                        params=f'\nPARAMS: {params}\n' if params else '',
                        status=r.status)
                    )

                    # even errors have text involved in them so this is safe to call
                    data = await json_or_text(r)

                    # the request was successful so just return the text/json
                    if 300 > r.status >= 200:
                        log.debug(f'{method} {url} has received {data}')
                        return data

                    # we are being rate limited
                    if r.status == 429:
                        # I haven't been able to get any X-Retry-After headers
                        # from the API but we should probably still handle it
                        try:
                            await asyncio.sleep(float(r.headers['X-Retry-After']))
                        except KeyError:  # steam being un-helpful as usual
                            await asyncio.sleep(2 ** tries)
                        continue

                    # we've received a 500 or 502, an unconditional retry
                    if r.status in {500, 502}:
                        await asyncio.sleep(1 + tries * 3)
                        continue

                    if r.status == 401:
                        # api key either got revoked or it was never valid
                        if not data:
                            raise errors.HTTPException(r, data)
                        if 'Access is denied. Retrying will not help. Please verify your <pre>key=</pre>' in data:
                            # time to fetch a new key
                            self.api_key = await self.get_api_key()
                            kwargs['key'] = self.api_key
                            continue  # retry with our new key

                    # the usual error cases
                    if r.status == 403:
                        raise errors.Forbidden(r, data)
                    elif r.status == 404:
                        raise errors.NotFound(r, data)
                    else:
                        raise errors.HTTPException(r, data)

            # we've run out of retries, raise
            raise errors.HTTPException(r, data)

    def connect_to_cm(self, cm) -> Awaitable:
        headers = {
            "User-Agent": self.user_agent
        }
        return self._session.ws_connect(cm, timeout=60, autoclose=False, headers=headers)

    async def login(self, username: str, password: str, api_key: str, shared_secret: str = None) -> None:
        self.username = username
        self.password = password
        self.shared_secret = shared_secret

        login_response = await self._send_login_request()

        if 'captcha_needed' in login_response:
            raise errors.LoginError('A captcha code is required, please try again later')
        if not login_response['success']:
            raise errors.InvalidCredentials(login_response['message'])

        data = login_response.get('transfer_parameters')
        if data is None:
            raise errors.LoginError('Cannot perform redirects after login, no parameters fetched. '
                                    'The Steam API likely is down, please try again later.')

        for url in login_response['transfer_urls']:
            await self.request('POST', url=url, data=data)
        self.logged_in = True

        if api_key is None:
            self._client.api_key = await self.get_api_key()
        else:
            self._client.api_key = api_key
            resp = await self.request('GET', f'{URL.COMMUNITY}/account/history')
            search = re.search(r'g_sessionID = "(?P<sessionID>.*?)";', resp)
            self.session_id = search.group('sessionID')
        self.api_key = self._client.api_key
        self._state = self._client._connection

        id64 = login_response['transfer_parameters']['steamid']
        resp = await self.get_profile(id64)
        data = resp['response']['players'][0]
        self.user = ClientUser(state=self._state, data=data)
        await self.user.__ainit__()
        self._client.dispatch('login')

    async def logout(self) -> None:
        log.debug('Logging out of session')
        payload = {
            "sessionid": self.session_id
        }
        await self.request('POST', url=f'{URL.COMMUNITY}/login/logout', data=payload)
        self.logged_in = False
        self._client.dispatch('logout')

    async def _get_rsa_params(self, current_repetitions: int = 0) -> Tuple['RsaKey', int]:
        maximum_repetitions = 5
        payload = {
            "username": self.username,
            "donotcache": int(time() * 1000)
        }
        try:
            key_response = await self.request('POST', url=f'{URL.COMMUNITY}/login/getrsakey', data=payload)
        except Exception as e:
            raise errors.LoginError from e
        try:
            rsa_mod = int(key_response['publickey_mod'], 16)
            rsa_exp = int(key_response['publickey_exp'], 16)
            rsa_timestamp = key_response['timestamp']
            return construct((rsa_mod, rsa_exp)), rsa_timestamp
        except KeyError:
            if current_repetitions < maximum_repetitions:
                return await self._get_rsa_params(current_repetitions + 1)
            else:
                raise ValueError('Could not obtain rsa-key')

    async def _send_login_request(self) -> dict:
        rsa_key, rsa_timestamp = await self._get_rsa_params()
        encrypted_password = b64encode(PKCS1_v1_5.new(rsa_key).encrypt(self.password.encode('ascii'))).decode()
        payload = {
            "username": self.username,
            "password": encrypted_password,
            "emailauth": '',
            "emailsteamid": '',
            "twofactorcode": self._one_time_code or '',
            "captchagid": '-1',
            "captcha_text": '',
            "loginfriendlyname": self.user_agent,
            "rsatimestamp": rsa_timestamp,
            "remember_login": True,
            "donotcache": int(time() * 1000),
        }
        try:
            login_response = await self.request('POST', url=f'{URL.COMMUNITY}/login/dologin', data=payload)
            if login_response['requires_twofactor']:
                self._one_time_code = await self._client.code()
                return await self._send_login_request()
            return login_response
        except Exception as e:
            raise errors.HTTPException from e

    def get_profile(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamids": user_id64
        }
        return self.request('GET', url=Route('ISteamUser', 'GetPlayerSummaries', 'v2'), params=params)

    async def get_profiles(self, user_id64s: List[int]) -> List[dict]:
        ret = []

        def chunk():  # chunk the list into 100 element sub-lists for the requests
            for i in range(0, len(user_id64s), 100):
                yield user_id64s[i:i + 100]

        for sublist in chunk():
            for _ in sublist:
                params = {
                    "key": self.api_key,
                    "steamids": ','.join(map(str, sublist))
                }

            full_resp = await self.request('GET', Route('ISteamUser', 'GetPlayerSummaries', 'v2'), params=params)
            ret.extend([user for user in full_resp['response']['players']])
        return ret

    def add_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "accept_invite": 0
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/AddFriendAjax', json=payload)

    def remove_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/RemoveFriendAjax', json=payload)

    def block_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "block": 1
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/BlockUserAjax', json=payload)

    def unblock_user(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "block": 0
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/BlockUserAjax', json=payload)

    def accept_user_invite(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "accept_invite": 1
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/AddFriendAjax', json=payload)

    def decline_user_invite(self, user_id64: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "steamid": user_id64,
            "accept_invite": 0
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/IgnoreFriendInviteAjax', json=payload)

    def get_user_games(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64,
            "include_appinfo": 1,
            "include_played_free_games": 1
        }
        return self.request('GET', url=Route('IPlayerService', 'GetOwnedGames'), params=params)

    def get_user_inventory(self, user_id64: int, app_id: int, context_id: int) -> Awaitable:
        params = {
            "count": 5000,
        }
        return self.request('GET', url=f'{URL.COMMUNITY}/inventory/{user_id64}/{app_id}/{context_id}', params=params)

    def get_user_escrow(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid_target": user_id64
        }
        return self.request('GET', url=Route('IEconService', 'GetTradeHoldDurations'), params=params)

    async def get_friends(self, user_id64: int) -> List[dict]:
        params = {
            "key": self.api_key,
            "steamid": user_id64,
            "relationship": 'friend'
        }
        friends = await self.request('GET', url=Route('ISteamUser', 'GetFriendList'), params=params)
        return await self.get_profiles([friend['steamid'] for friend in friends['friendslist']['friends']])

    def get_trade_offers(self, active_only: bool = True,
                         sent: bool = True, received: bool = True) -> Awaitable:
        params = {
            "key": self.api_key,
            "active_only": int(active_only),
            "get_sent_offers": int(sent),
            "get_descriptions": 1,
            "get_received_offers": int(received)
        }
        return self.request('GET', url=Route('IEconService', 'GetTradeOffers'), params=params)

    def get_trade_history(self, limit: int, previous_time: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "max_trades": limit,
            "get_descriptions": 1,
            "include_total": 1,
            "start_after_time": previous_time or 0
        }
        return self.request('GET', url=Route('IEconService', 'GetTradeHistory'), params=params)

    def get_trade(self, trade_id: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "tradeofferid": trade_id,
            "get_descriptions": 1
        }
        return self.request('GET', url=Route('IEconService', 'GetTradeOffer'), params=params)

    def accept_user_trade(self, user_id64: int, trade_id: int) -> Awaitable:
        payload = {
            'sessionid': self.session_id,
            'tradeofferid': trade_id,
            'serverid': 1,
            'partner': user_id64,
            'captcha': ''
        }
        headers = {'Referer': f'{URL.COMMUNITY}/tradeoffer/{trade_id}'}
        return self.request('POST', url=f'{URL.COMMUNITY}/tradeoffer/{trade_id}/accept', json=payload, headers=headers)

    def decline_user_trade(self, trade_id: int) -> Awaitable:
        payload = {
            "key": self.api_key,
            "tradeofferid": trade_id
        }
        return self.request('POST', url=Route('IEconService', 'DeclineTradeOffer'), json=payload)

    def cancel_user_trade(self, trade_id: int) -> Awaitable:
        payload = {
            "key": self.api_key,
            "tradeofferid": trade_id
        }
        return self.request('POST', url=Route('IEconService', 'CancelTradeOffer'), json=payload)

    def send_trade_offer(self, user_id64: int, user_id: int,
                         to_send: List[dict], to_receive: List[dict],
                         token: Optional[str], offer_message: str,
                         **kwargs) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "serverid": 1,
            "partner": user_id64,
            "tradeoffermessage": offer_message,
            "json_tradeoffer": json.dumps({
                "newversion": True,
                "version": 4,
                "me": {
                    "assets": to_send,
                    "currency": [],
                    "ready": False
                },
                "them": {
                    "assets": to_receive,
                    "currency": [],
                    "ready": False
                }
            }),
            "captcha": '',
            "trade_offer_create_params": json.dumps({
                'trade_offer_access_token': token
            }) if token is not None else {}
        }
        payload.update(**kwargs)
        headers = {'Referer': f'{URL.COMMUNITY}/tradeoffer/new/?partner={user_id}'}
        return self.request('POST', url=f'{URL.COMMUNITY}/tradeoffer/new/send', json=payload, headers=headers)

    def send_counter_trade_offer(self, trade_id: int, user_id64: int, user_id: int,
                                 to_send: List[dict], to_receive: List[dict],
                                 token: Optional[str], offer_message: str) -> Awaitable:
        return self.send_trade_offer(user_id64, user_id, to_send, to_receive, token, offer_message, trade_id=trade_id)

    def get_cm_list(self, cell_id: int) -> Awaitable:
        params = {
            "cellid": cell_id
        }
        return self.request('GET', url=Route('ISteamDirectory', 'GetCMList'), params=params)

    def get_comments(self, id64: int, comment_type: str, limit: int = None) -> Awaitable:
        params = {
            "start": 0,
            "totalcount": 9999999999
        }
        if limit is None:
            params["count"] = 9999999999
        else:
            params["count"] = limit
        return self.request('GET', f'{URL.COMMUNITY}/comment/{comment_type}/render/{id64}', params=params)

    def post_comment(self, id64: int, comment_type: str, content: str) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "comment": content,
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/comment/{comment_type}/post/{id64}', json=payload)

    def delete_comment(self, id64: int, comment_id: int, comment_type: str) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "gidcomment": comment_id,
        }
        return self.request('POST', f'{URL.COMMUNITY}/comment/{comment_type}/delete/{id64}', json=payload)

    def report_comment(self, id64: int, comment_id: int, comment_type: str) -> Awaitable:
        payload = {
            "gidcomment": comment_id,
            "hide": 1
        }
        return self.request('POST', f'{URL.COMMUNITY}/comment/{comment_type}/hideandreport/{id64}', json=payload)

    async def get_api_key(self) -> str:
        resp = await self.request('GET', url=f'{URL.COMMUNITY}/dev/apikey')
        error = 'You must have a validated email address to create a Steam Web API key'
        if error in resp:
            raise errors.LoginError(error)

        match = re.findall(r'<p>Key: ([0-9A-F]+)</p>', resp)
        if match:
            search = re.search(r'g_sessionID = "(?P<sessionID>.*?)";', resp)
            self.session_id = search.group('sessionID')
            return match[0]
        else:
            payload = {
                "domain": 'steam.py',
                "agreeToTerms": 'agreed',
                "sessionid": self.session_id,
                "Submit": 'Register'
            }
            await self.request('POST', url=f'{URL.COMMUNITY}/dev/registerkey', json=payload)
            return await self.get_api_key()

    def accept_group_invite(self, group_id: int) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "steamid": self.user.id64,
            "ajax": '1',
            "action": 'group_accept',
            "steamids[]": group_id
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/me/friends/action', json=payload)

    def decline_group_invite(self, group_id: int) -> Awaitable:
        payload = {
            "sessionid": self.session_id,
            "steamid": self.user.id64,
            "ajax": '1',
            "action": 'group_ignore',
            "steamids[]": group_id
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/me/friends/action', json=payload)

    def join_group(self, group_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "action": 'join',
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/gid/{group_id}', json=payload)

    def leave_group(self, group_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "action": 'leaveGroup',
            "groupId": group_id
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/me/home_process', json=payload)

    def invite_user_to_group(self, user_id64: int, group_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "group": group_id,
            "invitee": user_id64,
            "type": 'groupInvite',
            "json": 1,
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/actions/GroupInvite', json=payload)

    def get_user_groups(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64
        }
        return self.request('GET', url=Route('ISteamUser', 'GetUserGroupList'), params=params)

    def get_user_bans(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamids": user_id64
        }
        return self.request('GET', url=Route('ISteamUser', 'GetPlayerBans'), params=params)

    def get_user_level(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64
        }
        return self.request('GET', url=Route('IPlayerService', 'GetSteamLevel'), params=params)

    def get_user_badges(self, user_id64: int) -> Awaitable:
        params = {
            "key": self.api_key,
            "steamid": user_id64
        }
        return self.request('GET', url=Route('IPlayerService', 'GetBadges'), params=params)

    def clear_nickname_history(self) -> Awaitable:
        payload = {
            "sessionid": self.session_id
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/me/ajaxclearaliashistory', json=payload)

    def edit_profile(self, nick: str, real_name: str, country: str, summary: str, group_id: int) -> Awaitable:
        payload = {
            "sessionID": self.session_id,
            "type": 'profileSave',
            "personaName": nick,
            "real_name": real_name,
            "country": country,
            "summary": summary,
            "primary_group_steamid": group_id
        }
        return self.request('POST', url=f'{URL.COMMUNITY}/me/edit', json=payload)

    async def send_image(self, user_id64: int, image: 'Image') -> None:
        referer = {
            "Referer": f'{URL.COMMUNITY}/chat',
        }

        data = aiohttp.FormData()
        data.add_field('sessionid', self.session_id)
        data.add_field('l', 'english')
        data.add_field('file_size', len(image))
        data.add_field('file_name', image.name)
        data.add_field('file_sha', image.hash)
        data.add_field('file_image_width', image.width)
        data.add_field('file_image_height', image.height)
        data.add_field('file_type', f'image/{image.type}')
        resp = await self.request('POST', f'{URL.COMMUNITY}/chat/beginfileupload?l=english', headers=referer, data=data)

        result = resp['result']
        url = f'{"https" if result["use_https"] else "http"}://{result["url_host"]}{result["url_path"]}'
        headers = {header['name'].lower(): header['value'] for header in result['request_headers']}

        file_data = aiohttp.FormData()
        file_data.add_field('body', image.fp.read(), filename=image.name)
        await self.request('PUT', url=url, headers=headers, data=file_data)

        data._fields.pop(2)
        data.add_field('success', '1')
        data.add_field('ugcid', result['ugcid'])
        data.add_field('timestamp', resp['timestamp'])
        data.add_field('hmac', resp['hmac'])
        data.add_field('friend_steamid', user_id64)
        data.add_field('spoiler', int(image.spoiler))
        await self.request('POST', url=f'{URL.COMMUNITY}/chat/commitfileupload', data=data, headers=referer)