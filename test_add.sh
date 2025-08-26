#!/bin/bash
export NODE_ENV=test

# Test adding a single item
./add.sh "new item 1"
echo "List after adding a single item:"
./list.sh

# Test adding a single item with multiple words
./add.sh new item 2
echo "List after adding a single item with multiple words:"
./list.sh

# Test adding multiple items with commas
./add.sh "new item 3,new item 4"
echo "List after adding multiple items with commas:"
./list.sh

# Test adding multiple items with commas and spaces
./add.sh "new item 5", "new item 6"
echo "List after adding multiple items with commas and spaces:"
./list.sh

# Cleanup
# Get the current list to find the item numbers to remove
# This is a bit tricky, so for now I'll just remove by name, assuming the remove script can handle that.
# A more robust solution would be to get the list and parse the item numbers.
./remove.sh "new item 1"
./remove.sh "new item 2"
./remove.sh "new item 3"
./remove.sh "new item 4"
./remove.sh "new item 5"
./remove.sh "new item 6"