import os
import sys
import asyncio

from lib.anylist import AnyList
from lib.item import Item

# A simple function to prompt the user for input. In a real application,
# this would be more robust.
def promptUser(question):
    return input(question)

async def addItemToList(list_obj, item_name, anylist_instance):
    """
    Adds an item to the given list.
    """
    existing_item = list_obj.get_item_by_name(item_name)
    if existing_item:
        if existing_item.checked:
            existing_item.checked = False
            await existing_item.save()
            print(f'Item "{item_name}" readded to "{list_obj.name}".')
        else:
            print(f'Item "{item_name}" already exists in "{list_obj.name}".')
        return

    new_item = anylist_instance.create_item({'name': item_name})
    await list_obj.add_item(new_item)
    print(f'Item "{new_item.name}" added to "{list_obj.name}".')


async def main():
    """
    Main function to run the add item script.
    """
    # For testing purposes, we'll use hardcoded credentials.
    # In a real application, you would use a secure way to store and
    # retrieve credentials.
    email = os.environ.get('EMAIL', 'test@example.com')
    password = os.environ.get('PASSWORD', 'password')
    list_name = os.environ.get('PRIMARY_LIST_NAME', 'Test List')

    anylist = AnyList(email, password)

    try:
        await anylist.login()
        await anylist.get_lists()

        list_obj = anylist.get_list_by_name(list_name)

        if not list_obj:
            print(f'List "{list_name}" not found.')
            return

        args = sys.argv[1:]
        if args:
            for item_name in args:
                await addItemToList(list_obj, item_name, anylist)
        else:
            while True:
                try:
                    item_name = promptUser('Enter the item name (or "q" to quit): ')
                    if item_name.lower() in ['q', 'quit', 'exit']:
                        break
                    if item_name.strip():
                        await addItemToList(list_obj, item_name, anylist)
                except (EOFError, KeyboardInterrupt):
                    break
    finally:
        # In a real application, you would want to properly close any
        # connections.
        # The anylist library doesn't have an explicit teardown method,
        # but if it did, it would be called here.
        pass

if __name__ == '__main__':
    asyncio.run(main())
