import uuid

def uuid_v4():
    return str(uuid.uuid4()).replace('-', '')
