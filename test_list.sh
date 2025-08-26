#!/bin/bash
export NODE_ENV=test

# Add some items to the list to test with
./add.sh "item 1"
./add.sh "item 2"
./add.sh "item 3"

echo "Original list:"
./list.sh

echo -e "\nUpdating item 2 to \"updated item 2\""
./list.sh -u 2 updated item 2

echo -e "\nList after updating item 2:"
./list.sh

# Clean up the added items
./remove.sh "item 1"
./remove.sh "updated item 2"
./remove.sh "item 3"