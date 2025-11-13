import os
import sys
import asyncio
import argparse
from dotenv import load_dotenv

from lib.anylist import AnyList


def parse_args():
    parser = argparse.ArgumentParser(description='List active items from AnyList')
    parser.add_argument('-u', '--update', nargs='+', metavar=('ITEM_NUMBER', 'NEW_NAME'),
                       help='Update an item: -u <item_number> <new_item_name>')
    return parser.parse_args()


async def display_active_items(anylist, list_name):
    """Display active (unchecked) items from the specified list."""
    await anylist.login()
    await anylist.get_lists()

    list_obj = anylist.get_list_by_name(list_name)

    if not list_obj:
        print(f'List "{list_name}" not found.')
        return

    active_items = [item for item in list_obj.items if not item.checked]

    if not active_items:
        print(f'No active items in "{list_name}".')
    else:
        print(f'Active items in "{list_name}":')
        for index, item in enumerate(active_items, 1):
            print(f'{index}. {item.name}')


async def update_item(anylist, list_name, item_number, new_name):
    """Update a specific item's name."""
    await anylist.login()
    await anylist.get_lists()

    list_obj = anylist.get_list_by_name(list_name)

    if not list_obj:
        print(f'List "{list_name}" not found.')
        return

    active_items = [item for item in list_obj.items if not item.checked]

    if item_number < 1 or item_number > len(active_items):
        print(f'Invalid item number: {item_number}. There are only {len(active_items)} active items.')
        return

    item_to_update = active_items[item_number - 1]
    old_name = item_to_update.name
    item_to_update.name = new_name
    await item_to_update.save()

    print(f'Updated item {item_number} from "{old_name}" to "{new_name}".')


async def main():
    # Load environment variables
    load_dotenv()
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')
    list_name = os.environ.get('PRIMARY_LIST_NAME')

    if not email or not password or not list_name:
        print('Missing required environment variables: EMAIL, PASSWORD, PRIMARY_LIST_NAME')
        sys.exit(1)

    anylist = AnyList(email, password)

    args = parse_args()

    try:
        if args.update:
            # Update mode: -u <item_number> <new_name>
            if len(args.update) < 2:
                print('Error: -u requires both item number and new name.')
                sys.exit(1)

            try:
                item_number = int(args.update[0])
                new_name = ' '.join(args.update[1:])
                await update_item(anylist, list_name, item_number, new_name)
            except ValueError:
                print('Error: Item number must be an integer.')
                sys.exit(1)
        else:
            # Display mode
            await display_active_items(anylist, list_name)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())