class MealPlanningCalendarEventLabel:
    def __init__(self, label):
        if isinstance(label, dict):
            self.identifier = label.get('identifier')
            self.calendar_id = label.get('calendarId')
            self.hex_color = label.get('hexColor')
            self.logical_timestamp = label.get('logicalTimestamp')
            self.name = label.get('name')
            self.sort_index = label.get('sortIndex')
        else:
            self.identifier = label.identifier
            self.calendar_id = label.calendarId
            self.hex_color = label.hexColor
            self.logical_timestamp = label.logicalTimestamp
            self.name = label.name
            self.sort_index = label.sortIndex
