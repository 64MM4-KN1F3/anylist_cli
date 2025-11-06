from .uuid import uuid_v4

OP_MAPPING = {
    'name': 'set-list-item-name',
    'quantity': 'set-list-item-quantity',
    'details': 'set-list-item-details',
    'checked': 'set-list-item-checked',
    'categoryMatchId': 'set-list-item-category-match-id',
    'manualSortIndex': 'set-list-item-sort-order',
}

class Item:
    def __init__(self, i, client=None, protobuf=None, uid=None):
        if isinstance(i, dict):
            self._list_id = i.get('listId')
            self._identifier = i.get('identifier') or uuid_v4()
            self._name = i.get('name')
            self._details = i.get('details')
            self._quantity = i.get('quantity')
            self._checked = i.get('checked')
            self._manual_sort_index = i.get('manualSortIndex')
            self._user_id = i.get('userId')
            self._category_match_id = i.get('categoryMatchId') or 'other'
        else:
            self._list_id = i.listId
            self._identifier = i.identifier or uuid_v4()
            self._name = i.name
            self._details = i.details
            self._quantity = i.deprecatedQuantity
            self._checked = i.checked
            self._manual_sort_index = i.manualSortIndex
            self._user_id = i.userId
            self._category_match_id = i.categoryMatchId or 'other'

        self._client = client
        self._protobuf = protobuf
        self._uid = uid

        self._fields_to_update = []

    def to_json(self):
        return {
            'listId': self._list_id,
            'identifier': self._identifier,
            'name': self._name,
            'details': self._details,
            'quantity': self._quantity,
            'checked': self._checked,
            'manualSortIndex': self._manual_sort_index,
            'userId': self._user_id,
            'categoryMatchId': self._category_match_id,
        }

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, _):
        raise ValueError('You cannot update an item ID.')

    @property
    def list_id(self):
        return self._list_id

    @list_id.setter
    def list_id(self, l):
        if self._list_id is None:
            self._list_id = l
            self._fields_to_update.append('listId')
        else:
            raise ValueError('You cannot move items between lists.')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n
        self._fields_to_update.append('name')

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, q):
        if isinstance(q, (int, float)):
            q = str(q)

        self._quantity = q
        self._fields_to_update.append('quantity')

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, d):
        self._details = d
        self._fields_to_update.append('details')

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, c):
        if not isinstance(c, bool):
            raise TypeError('Checked must be a boolean.')

        self._checked = c
        self._fields_to_update.append('checked')

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, _):
        raise ValueError('Cannot set user ID of an item after creation.')

    @property
    def category_match_id(self):
        return self._category_match_id

    @category_match_id.setter
    def category_match_id(self, i):
        self._category_match_id = i
        self._fields_to_update.append('categoryMatchId')

    @property
    def manual_sort_index(self):
        return self._manual_sort_index

    @manual_sort_index.setter
    def manual_sort_index(self, i):
        if not isinstance(i, (int, float)):
            raise TypeError('Sort index must be a number.')

        self._manual_sort_index = i
        self._fields_to_update.append('manualSortIndex')

    async def save(self, is_favorite=False):
        # This is a placeholder for the actual save implementation
        pass
