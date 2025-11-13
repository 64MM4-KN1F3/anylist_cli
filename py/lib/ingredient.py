class Ingredient:
    def __init__(self, i, client=None, protobuf=None, uid=None):
        if isinstance(i, dict):
            self._raw_ingredient = i.get('rawIngredient')
            self._name = i.get('name')
            self._quantity = i.get('quantity')
            self._note = i.get('note')
        else:
            self._raw_ingredient = i.rawIngredient
            self._name = i.name
            self._quantity = i.quantity
            self._note = i.note

        self._client = client
        self._protobuf = protobuf
        self._uid = uid
        self._fields_to_update = []

    def to_json(self):
        return {
            'rawIngredient': self._raw_ingredient,
            'name': self._name,
            'quantity': self._quantity,
            'note': self._note,
        }

    @property
    def raw_ingredient(self):
        return self._raw_ingredient

    @raw_ingredient.setter
    def raw_ingredient(self, n):
        self._raw_ingredient = n
        self._fields_to_update.append('rawIngredient')

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
        self._quantity = q
        self._fields_to_update.append('quantity')

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, n):
        self._note = n
        self._fields_to_update.append('note')

    def _encode(self):
        return self._protobuf.PBIngredient(
            name=self._name,
            quantity=self._quantity,
            rawIngredient=self._raw_ingredient,
            note=self._note
        )
