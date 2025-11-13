from datetime import datetime
from .uuid import uuid_v4

class MealPlanningCalendarEvent:
    def __init__(self, event, client=None, protobuf=None, uid=None, calendar_id=None):
        if isinstance(event, dict):
            self.identifier = event.get('identifier', uuid_v4())
            self.date = event.get('date', datetime.now())
            self.details = event.get('details')
            self.label_id = event.get('labelId')
            self.logical_timestamp = event.get('logicalTimestamp')
            self.order_added_sort_index = event.get('orderAddedSortIndex')
            self.recipe_id = event.get('recipeId')
            self.recipe_scale_factor = event.get('recipeScaleFactor')
            self.title = event.get('title')
            self._is_new = 'identifier' not in event
        else:
            self.identifier = event.identifier or uuid_v4()
            self.date = datetime.strptime(event.date, '%Y-%m-%d')
            self.details = event.details
            self.label_id = event.labelId
            self.logical_timestamp = event.logicalTimestamp
            self.order_added_sort_index = event.orderAddedSortIndex
            self.recipe_id = event.recipeId
            self.recipe_scale_factor = event.recipeScaleFactor
            self.title = event.title
            self._is_new = not event.identifier

        self.recipe = None
        self.label = None
        self._client = client
        self._protobuf = protobuf
        self._uid = uid
        self._calendar_id = calendar_id

    def to_json(self):
        return {
            'identifier': self.identifier,
            'logicalTimestamp': self.logical_timestamp,
            'calendarId': self._calendar_id,
            'date': self.date.isoformat(),
            'title': self.title,
            'details': self.details,
            'recipeId': self.recipe_id,
            'labelId': self.label_id,
            'orderAddedSortIndex': self.order_added_sort_index,
            'recipeScaleFactor': self.recipe_scale_factor,
        }

    async def perform_operation(self, handler_id):
        from .uuid import uuid_v4

        op = self._protobuf.PBCalendarOperation()
        op.metadata.operationId = uuid_v4()
        op.metadata.handlerId = handler_id
        op.metadata.userId = self._uid

        op.calendarId = self._calendar_id
        op.updatedEvent.CopyFrom(self._encode())

        op_list = self._protobuf.PBCalendarOperationList()
        op_list.operations.extend([op])

        headers = {
            'X-AnyLeaf-Client-Identifier': self._client.client_id,
            'Authorization': f'Bearer {self._client.access_token}'
        }

        await self._client.post('data/meal-planning-calendar/update', headers=headers, content=op_list.SerializeToString())

    async def save(self):
        operation = 'new-event' if self._is_new else 'set-event-details'
        await self.perform_operation(operation)

    async def delete(self):
        await self.perform_operation('delete-event')

    def _encode(self):
        return self._protobuf.PBCalendarEvent(
            identifier=self.identifier,
            logicalTimestamp=self.logical_timestamp,
            calendarId=self._calendar_id,
            date=self.date.strftime('%Y-%m-%d'),
            title=self.title,
            details=self.details,
            recipeId=self.recipe_id,
            labelId=self.label_id,
            orderAddedSortIndex=self.order_added_sort_index,
            recipeScaleFactor=self.recipe_scale_factor,
        )
