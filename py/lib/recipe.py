from datetime import datetime
from lib.py.ingredient import Ingredient
from lib.py.uuid import uuid_v4

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
        # This is a placeholder for the actual perform_operation implementation
        pass

    async def save(self):
        await self.perform_operation('save-recipe')

    async def delete(self):
        await self.perform_operation('remove-recipe')
