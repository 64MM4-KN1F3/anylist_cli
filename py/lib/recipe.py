from datetime import datetime
from .ingredient import Ingredient
from .uuid import uuid_v4

class Recipe:
    def __init__(self, recipe, client=None, protobuf=None, uid=None, recipe_data_id=None):
        if isinstance(recipe, dict):
            self.identifier = recipe.get('identifier', uuid_v4())
            self.timestamp = recipe.get('timestamp', datetime.now().timestamp())
            self.name = recipe.get('name')
            self.note = recipe.get('note')
            self.source_name = recipe.get('sourceName')
            self.source_url = recipe.get('sourceUrl')
            self.ingredients = [Ingredient(i, client=client, protobuf=protobuf, uid=uid) for i in recipe.get('ingredients', [])]
            self.preparation_steps = recipe.get('preparationSteps', [])
            self.photo_ids = recipe.get('photoIds', [])
            self.photo_urls = recipe.get('photoUrls', [])
            self.ad_campaign_id = recipe.get('adCampaignId')
            self.scale_factor = recipe.get('scaleFactor')
            self.rating = recipe.get('rating')
            self.creation_timestamp = recipe.get('creationTimestamp')
            self.nutritional_info = recipe.get('nutritionalInfo')
            self.cook_time = recipe.get('cookTime')
            self.prep_time = recipe.get('prepTime')
            self.servings = recipe.get('servings')
            self.paprika_identifier = recipe.get('paprikaIdentifier')
        else:
            self.identifier = recipe.identifier or uuid_v4()
            self.timestamp = recipe.timestamp or datetime.now().timestamp()
            self.name = recipe.name
            self.note = recipe.note
            self.source_name = recipe.sourceName
            self.source_url = recipe.sourceUrl
            self.ingredients = [Ingredient(i, client=client, protobuf=protobuf, uid=uid) for i in recipe.ingredients]
            self.preparation_steps = recipe.preparationSteps
            self.photo_ids = recipe.photoIds
            self.photo_urls = recipe.photoUrls
            self.ad_campaign_id = recipe.adCampaignId
            self.scale_factor = recipe.scaleFactor
            self.rating = recipe.rating
            self.creation_timestamp = recipe.creationTimestamp
            self.nutritional_info = recipe.nutritionalInfo
            self.cook_time = recipe.cookTime
            self.prep_time = recipe.prepTime
            self.servings = recipe.servings
            self.paprika_identifier = recipe.paprikaIdentifier

        self._client = client
        self.protobuf = protobuf
        self.uid = uid
        self.recipe_data_id = recipe_data_id

    async def perform_operation(self, handler_id):
        from .uuid import uuid_v4

        op = self.protobuf.PBRecipeOperation()
        op.metadata.operationId = uuid_v4()
        op.metadata.handlerId = handler_id
        op.metadata.userId = self.uid

        op.recipeDataId = self.recipe_data_id
        op.recipe.CopyFrom(self._encode())

        op_list = self.protobuf.PBRecipeOperationList()
        op_list.operations.extend([op])

        headers = {
            'X-AnyLeaf-Client-Identifier': self._client.client_id,
            'Authorization': f'Bearer {self._client.access_token}'
        }

        await self._client.post('data/user-recipe-data/update', headers=headers, content=op_list.SerializeToString())

    async def save(self):
        await self.perform_operation('save-recipe')

    async def delete(self):
        await self.perform_operation('remove-recipe')

    def _encode(self):
        return self.protobuf.PBRecipe(
            identifier=self.identifier,
            timestamp=self.timestamp,
            name=self.name,
            note=self.note,
            sourceName=self.source_name,
            sourceUrl=self.source_url,
            ingredients=[i._encode() for i in self.ingredients],
            preparationSteps=self.preparation_steps,
            photoIds=self.photo_ids,
            adCampaignId=self.ad_campaign_id,
            photoUrls=self.photo_urls,
            scaleFactor=self.scale_factor,
            rating=self.rating,
            creationTimestamp=self.creation_timestamp,
            nutritionalInfo=self.nutritional_info,
            cookTime=self.cook_time,
            prepTime=self.prep_time,
            servings=self.servings,
            paprikaIdentifier=self.paprika_identifier,
        )
