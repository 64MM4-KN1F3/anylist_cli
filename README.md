# Basic AnyList CLI

## Details
This *very* basic CLI uses unpublished API endpoints discovered and wrapped as a node package by codetheweb: https://github.com/codetheweb/anylist

## Prereqs

Install in the current path using:
```shell
git clone https://github.com/64MM4-KN1F3/anylist_cli.git
```

### .env
Create a .env file with the following lines:
```shell
EMAIL=<your_anylist_username>
PASSWORD=<your_anylist_password>
PRIMARY_LIST_NAME=<the_list_you_want_to_manage_via_CLI>
```

### package.json
To get dependencies, run: 
```shell
% npm install
```

## Usage
Run:
```shell
% node anyList_CLI.js
```

And away you go. Start adding items!

To quit, type: 'q', 'quit' or 'exit'
