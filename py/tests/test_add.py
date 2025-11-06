import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os
import asyncio

# Add the parent directory to the path so we can import the add module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add import main

class TestAdd(unittest.TestCase):

    @patch('add.AnyList')
    @patch('add.promptUser', side_effect=['test_item', 'q'])
    def test_add_item_interactive(self, mock_prompt, mock_anylist):
        """
        Tests adding a single item in interactive mode.
        """
        # Mock the AnyList object and its methods
        mock_list = MagicMock()
        mock_list.name = 'Test List'
        mock_anylist.return_value.login = AsyncMock()
        mock_anylist.return_value.get_lists = AsyncMock()
        mock_anylist.return_value.get_list_by_name.return_value = mock_list
        mock_list.get_item_by_name.return_value = None
        mock_list.add_item = AsyncMock()

        mock_item = MagicMock()
        mock_item.name = 'test_item'
        mock_anylist.return_value.create_item.return_value = mock_item

        # Mock sys.argv
        sys.argv = ['add.py']

        # Call the main function
        asyncio.run(main())

        # Assert that the item was added
        mock_list.add_item.assert_called_once()
        self.assertEqual(mock_list.add_item.call_args[0][0].name, 'test_item')

    @patch('add.AnyList')
    def test_add_item_single_arg(self, mock_anylist):
        """
        Tests adding a single item as a command-line argument.
        """
        # Mock the AnyList object and its methods
        mock_list = MagicMock()
        mock_list.name = 'Test List'
        mock_anylist.return_value.login = AsyncMock()
        mock_anylist.return_value.get_lists = AsyncMock()
        mock_anylist.return_value.get_list_by_name.return_value = mock_list
        mock_list.get_item_by_name.return_value = None
        mock_list.add_item = AsyncMock()

        mock_item = MagicMock()
        mock_item.name = 'test_item_arg'
        mock_anylist.return_value.create_item.return_value = mock_item

        # Mock sys.argv
        sys.argv = ['add.py', 'test_item_arg']

        # Call the main function
        asyncio.run(main())

        # Assert that the item was added
        mock_list.add_item.assert_called_once()
        self.assertEqual(mock_list.add_item.call_args[0][0].name, 'test_item_arg')


    @patch('add.AnyList')
    def test_add_multiple_items_args(self, mock_anylist):
        """
        Tests adding multiple items as command-line arguments.
        """
        # Mock the AnyList object and its methods
        mock_list = MagicMock()
        mock_list.name = 'Test List'
        mock_anylist.return_value.login = AsyncMock()
        mock_anylist.return_value.get_lists = AsyncMock()
        mock_anylist.return_value.get_list_by_name.return_value = mock_list
        mock_list.get_item_by_name.return_value = None
        mock_list.add_item = AsyncMock()

        mock_item1 = MagicMock()
        mock_item1.name = 'item1'
        mock_item2 = MagicMock()
        mock_item2.name = 'item2'
        mock_item3 = MagicMock()
        mock_item3.name = 'item3'
        mock_anylist.return_value.create_item.side_effect = [mock_item1, mock_item2, mock_item3]

        # Mock sys.argv
        sys.argv = ['add.py', 'item1', 'item2', 'item3']

        # Call the main function
        asyncio.run(main())

        # Assert that the items were added
        self.assertEqual(mock_list.add_item.call_count, 3)
        self.assertEqual(mock_list.add_item.call_args_list[0][0][0].name, 'item1')
        self.assertEqual(mock_list.add_item.call_args_list[1][0][0].name, 'item2')
        self.assertEqual(mock_list.add_item.call_args_list[2][0][0].name, 'item3')


    @patch('add.AnyList')
    def test_add_item_already_exists(self, mock_anylist):
        """
        Tests adding an item that already exists in the list.
        """
        # Mock the AnyList object and its methods
        mock_list = MagicMock()
        mock_list.name = 'Test List'
        mock_item = MagicMock()
        mock_item.checked = False
        mock_anylist.return_value.login = AsyncMock()
        mock_anylist.return_value.get_lists = AsyncMock()
        mock_anylist.return_value.get_list_by_name.return_value = mock_list
        mock_list.get_item_by_name.return_value = mock_item
        mock_list.add_item = AsyncMock()

        # Mock sys.argv
        sys.argv = ['add.py', 'existing_item']

        # Call the main function
        asyncio.run(main())

        # Assert that addItem was not called
        mock_list.add_item.assert_not_called()
        mock_item.save.assert_not_called()


    @patch('add.AnyList')
    def test_readd_checked_item(self, mock_anylist):
        """
        Tests re-adding an item that already exists but is checked.
        """
        # Mock the AnyList object and its methods
        mock_list = MagicMock()
        mock_list.name = 'Test List'
        mock_item = MagicMock()
        mock_item.checked = True
        mock_item.save = AsyncMock()
        mock_anylist.return_value.login = AsyncMock()
        mock_anylist.return_value.get_lists = AsyncMock()
        mock_anylist.return_value.get_list_by_name.return_value = mock_list
        mock_list.get_item_by_name.return_value = mock_item
        mock_list.add_item = AsyncMock()

        # Mock sys.argv
        sys.argv = ['add.py', 'checked_item']

        # Call the main function
        asyncio.run(main())

        # Assert that addItem was not called, but the item was unchecked and saved
        mock_list.add_item.assert_not_called()
        self.assertFalse(mock_item.checked)
        mock_item.save.assert_called_once()

if __name__ == '__main__':
    unittest.main()
