from .item import Item

class List:
    def __init__(self, list_data, client=None, protobuf=None, uid=None):
        if isinstance(list_data, dict):
            self.identifier = list_data.get('identifier')
            self.parent_id = list_data.get('listId')
            self.name = list_data.get('name')
            self.items = [Item(i, client=client, protobuf=protobuf, uid=uid) for i in list_data.get('items', [])]
        else:
            self.identifier = list_data.identifier
            self.parent_id = list_data.listId
            self.name = list_data.name
            self.items = [Item(i, client=client, protobuf=protobuf, uid=uid) for i in list_data.items]

        self.client = client
        self.protobuf = protobuf
        self.uid = uid

    async def add_item(self, item, is_favorite=False):
        if not isinstance(item, Item):
            raise TypeError('Must be an instance of the Item class.')

        item.list_id = self.identifier

        self.items.append(item)

        # In a real implementation, this would send a request to the AnyList API
        # to add the item to the list. For now, we'll just return the item.
        # Example:
        # await self.client.post(f'/lists/{self.identifier}/items', data=item.to_json())
        return item

    async def uncheck_all(self):
        # This is a placeholder for the actual uncheck_all implementation
        pass

    async def remove_item(self, item, is_favorite=False):
        # This is a placeholder for the actual remove_item implementation
        self.items = [i for i in self.items if i.identifier != item.identifier]

    def get_item_by_id(self, identifier):
        return next((i for i in self.items if i.identifier == identifier), None)

    def get_item_by_name(self, name):
        return next((i for i in self.items if i.name == name), None)
