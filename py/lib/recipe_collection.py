from datetime import datetime
from .uuid import uuid_v4

class RecipeCollection:
    def __init__(self, recipe_collection, client=None, protobuf=None, uid=None, recipe_data_id=None):
        self._client = client
        self.protobuf = protobuf
        self.uid = uid
        self.recipe_data_id = recipe_data_id

        self.identifier = recipe_collection.get('identifier', uuid_v4())
        self.timestamp = recipe_collection.get('timestamp', datetime.now().timestamp())
        self.name = recipe_collection.get('name')
        self.recipe_ids = recipe_collection.get('recipeIds', [])
        self.collection_settings = recipe_collection.get('collectionSettings', None) # Replace with protobuf equivalent

    async def perform_operation(self, handler_id):
        from .uuid import uuid_v4

        op = self.protobuf.PBRecipeOperation()
        op.metadata.operationId = uuid_v4()
        op.metadata.handlerId = handler_id
        op.metadata.userId = self.uid

        op.recipeDataId = self.recipe_data_id
        op.recipeCollection.CopyFrom(self._encode())

        op_list = self.protobuf.PBRecipeOperationList()
        op_list.operations.extend([op])

        headers = {
            'X-AnyLeaf-Client-Identifier': self._client.client_id,
            'Authorization': f'Bearer {self._client.access_token}'
        }

        await self._client.post('data/user-recipe-data/update', headers=headers, content=op_list.SerializeToString())

    async def save(self):
        await self.perform_operation('new-recipe-collection')

    async def delete(self):
        await self.perform_operation('remove-recipe-collection')

    async def add_recipe(self, recipe_id):
        if recipe_id:
            self.recipe_ids.append(recipe_id)
            await self.perform_operation('add-recipes-to-collection')

    async def remove_recipe(self, recipe_id):
        if recipe_id in self.recipe_ids:
            await self.perform_operation('remove-recipes-from-collection')
            self.recipe_ids.remove(recipe_id)

    def _encode(self):
        return self.protobuf.PBRecipeCollection(
            identifier=self.identifier,
            timestamp=self.timestamp,
            name=self.name,
            recipeIds=self.recipe_ids,
            collectionSettings=self.collection_settings,
        )
