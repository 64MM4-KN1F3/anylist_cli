import json
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import httpx
from lib.py import anylist_pb2

from lib.py.uuid import uuid_v4

CREDENTIALS_KEY_CLIENT_ID = 'clientId'
CREDENTIALS_KEY_ACCESS_TOKEN = 'accessToken'
CREDENTIALS_KEY_REFRESH_TOKEN = 'refreshToken'

class AnyList:
    def __init__(self, email, password, credentials_file=os.path.join(os.path.expanduser('~'), '.anylist_credentials')):
        self.email = email
        self.password = password
        self.credentials_file = credentials_file
        self.client_id = None
        self.access_token = None
        self.refresh_token = None
        self.lists = []
        self.favorite_items = []
        self.recent_items = {}
        self.recipes = []
        self.recipe_data_id = None
        self._user_data = None
        self.calendar_id = None

        self.auth_client = httpx.AsyncClient(base_url='https://www.anylist.com')
        self.auth_client.headers.update({'X-AnyLeaf-API-Version': '3'})

        self.client = httpx.AsyncClient(base_url='https://www.anylist.com')
        self.client.headers = self.auth_client.headers.copy()

        self.protobuf = anylist_pb2

    async def login(self, connect_web_socket=True):
        await self._load_credentials()
        self.client_id = await self._get_client_id()

        if not self.access_token or not self.refresh_token:
            await self._fetch_tokens()

        if connect_web_socket:
            self._setup_web_socket()

    async def _fetch_tokens(self):
        form = {
            'email': self.email,
            'password': self.password
        }

        response = await self.auth_client.post('/auth/token', data=form)
        result = response.json()

        self.access_token = result.get('access_token')
        self.refresh_token = result.get('refresh_token')
        await self._store_credentials()

    async def _refresh_tokens(self):
        form = {
            'refresh_token': self.refresh_token
        }

        try:
            response = await self.auth_client.post('/auth/token/refresh', data=form)
            response.raise_for_status()
            result = response.json()

            self.access_token = result.get('access_token')
            self.refresh_token = result.get('refresh_token')
            await self._store_credentials()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                await self._fetch_tokens()
            else:
                raise e

    async def _get_client_id(self):
        if self.client_id:
            return self.client_id

        client_id = uuid_v4()
        self.client_id = client_id
        await self._store_credentials()
        return client_id

    async def _load_credentials(self):
        if not self.credentials_file or not os.path.exists(self.credentials_file):
            return

        try:
            with open(self.credentials_file, 'rb') as f:
                encrypted = f.read()
            credentials = self._decrypt_credentials(encrypted, self.password)
            self.client_id = credentials.get(CREDENTIALS_KEY_CLIENT_ID)
            self.access_token = credentials.get(CREDENTIALS_KEY_ACCESS_TOKEN)
            self.refresh_token = credentials.get(CREDENTIALS_KEY_REFRESH_TOKEN)
        except Exception as e:
            print(f"Failed to read stored credentials: {e}")

    async def _store_credentials(self):
        if not self.credentials_file:
            return

        credentials = {
            CREDENTIALS_KEY_CLIENT_ID: self.client_id,
            CREDENTIALS_KEY_ACCESS_TOKEN: self.access_token,
            CREDENTIALS_KEY_REFRESH_TOKEN: self.refresh_token,
        }
        try:
            encrypted = self._encrypt_credentials(credentials, self.password)
            with open(self.credentials_file, 'wb') as f:
                f.write(encrypted)
        except Exception as e:
            print(f"Failed to write credentials to storage: {e}")

    def _encrypt_credentials(self, credentials, secret):
        plain = json.dumps(credentials).encode()
        key = hashlib.sha256(str(secret).encode()).digest()[:32]
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plain) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return json.dumps({'iv': iv.hex(), 'cipher': encrypted.hex()}).encode()

    def _decrypt_credentials(self, credentials, secret):
        encrypted = json.loads(credentials)
        key = hashlib.sha256(str(secret).encode()).digest()[:32]
        iv = bytes.fromhex(encrypted['iv'])
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(bytes.fromhex(encrypted['cipher'])) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plain = unpadder.update(padded_plain) + unpadder.finalize()
        return json.loads(plain.decode())

    def _setup_web_socket(self):
        # Placeholder
        pass

    async def get_lists(self, refresh_cache=True):
        from lib.py.list import List
        from lib.py.item import Item

        decoded = await self._get_user_data(refresh_cache)

        self.lists = [List(list_proto, self) for list_proto in decoded.shoppingListsResponse.newLists]

        for response in decoded.starterListsResponse.recentItemListsResponse.listResponses:
            list_proto = response.starterList
            self.recent_items[list_proto.listId] = [Item(item_proto, self) for item_proto in list_proto.items]

        favorite_lists = [object.starterList for object in decoded.starterListsResponse.favoriteItemListsResponse.listResponses]

        self.favorite_items = [List(list_proto, self) for list_proto in favorite_lists]

        return self.lists

    async def get_meal_planning_calendar_events(self, refresh_cache=True):
        from lib.py.meal_planning_calendar_event import MealPlanningCalendarEvent
        from lib.py.meal_planning_calendar_label import MealPlanningCalendarEventLabel
        from lib.py.recipe import Recipe

        decoded = await self._get_user_data(refresh_cache)

        self.meal_planning_calendar_events = [MealPlanningCalendarEvent(event, self) for event in decoded.mealPlanningCalendarResponse.events]

        self.meal_planning_calendar_event_labels = [MealPlanningCalendarEventLabel(label) for label in decoded.mealPlanningCalendarResponse.labels]
        for event in self.meal_planning_calendar_events:
            event.label = next((label for label in self.meal_planning_calendar_event_labels if label.identifier == event.label_id), None)

        self.recipes = [Recipe(recipe, self) for recipe in decoded.recipeDataResponse.recipes]
        for event in self.meal_planning_calendar_events:
            event.recipe = next((recipe for recipe in self.recipes if recipe.identifier == event.recipe_id), None)

        return self.meal_planning_calendar_events

    async def get_recipes(self, refresh_cache=True):
        from lib.py.recipe import Recipe

        decoded = await self._get_user_data(refresh_cache)

        self.recipes = [Recipe(recipe_proto, self) for recipe_proto in decoded.recipeDataResponse.recipes]
        self.recipe_data_id = decoded.recipeDataResponse.recipeDataId
        return self.recipes

    async def _get_user_data(self, refresh_cache):
        if not self._user_data or refresh_cache:
            headers = {
                'X-AnyLeaf-Client-Identifier': self.client_id,
                'Authorization': f'Bearer {self.access_token}'
            }
            result = await self.client.post('/data/user-data/get', headers=headers)
            self._user_data = self.protobuf.PBUserDataResponse()
            self._user_data.ParseFromString(result.content)
            self.calendar_id = self._user_data.mealPlanningCalendarResponse.calendarId

        return self._user_data
