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
        from .uuid import uuid_v4

        if not isinstance(item, Item):
            raise TypeError('Must be an instance of the Item class.')

        item.list_id = self.identifier

        op = self.protobuf.PBListOperation()
        op.metadata.operationId = uuid_v4()
        op.metadata.handlerId = 'add-item' if is_favorite else 'add-shopping-list-item'
        op.metadata.userId = self.uid

        op.listId = self.identifier
        op.listItemId = item.identifier
        op.listItem.CopyFrom(item._encode())

        op_list = self.protobuf.PBListOperationList()
        op_list.operations.extend([op])

        headers = {
            'X-AnyLeaf-Client-Identifier': self.client.client_id,
            'Authorization': f'Bearer {self.client.access_token}'
        }

        url = 'data/starter-lists/update' if is_favorite else 'data/shopping-lists/update'
        await self.client.post(url, headers=headers, content=op_list.SerializeToString())

        self.items.append(item)
        return item

    async def uncheck_all(self):
        # This is a placeholder for the actual uncheck_all implementation
        pass

    async def remove_item(self, item, is_favorite=False):
        from .uuid import uuid_v4

        op = self.protobuf.PBListOperation()
        op.metadata.operationId = uuid_v4()
        op.metadata.handlerId = 'remove-item' if is_favorite else 'remove-shopping-list-item'
        op.metadata.userId = self.uid

        op.listId = self.identifier
        op.listItemId = item.identifier
        op.listItem.CopyFrom(item._encode())

        op_list = self.protobuf.PBListOperationList()
        op_list.operations.extend([op])

        headers = {
            'X-AnyLeaf-Client-Identifier': self.client.client_id,
            'Authorization': f'Bearer {self.client.access_token}'
        }

        url = 'data/starter-lists/update' if is_favorite else 'data/shopping-lists/update'
        await self.client.post(url, headers=headers, content=op_list.SerializeToString())

        self.items = [i for i in self.items if i.identifier != item.identifier]

    def get_item_by_id(self, identifier):
        return next((i for i in self.items if i.identifier == identifier), None)

    def get_item_by_name(self, name):
        return next((i for i in self.items if i.name == name), None)
