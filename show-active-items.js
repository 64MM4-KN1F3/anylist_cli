const AnyList = require('anylist');
const dotenv = require('dotenv');
const fs = require('fs');

// Load environment variables
dotenv.config();

// Configure AnyList with credentials from .env
const anylist = new AnyList({
  email: process.env.EMAIL,
  password: process.env.PASSWORD
});

async function displayActiveItems() {
  try {
    await anylist.login();
    await anylist.getLists();

    const listName = process.env.PRIMARY_LIST_NAME;
    const list = anylist.getListByName(listName);

    if (!list) {
      console.error(`List "${listName}" not found`);
      await anylist.teardown();
      process.exit(1);
    }

    const activeItems = list.items.filter(item => !item.checked);

    if (activeItems.length === 0) {
      console.log(`No active items in "${listName}"`);
    } else {
      console.log(`Active items in "${listName}":`);
      activeItems.forEach((item, index) => {
        console.log(`${index + 1}. ${item.name}`);
      });
    }

    await anylist.teardown();
    process.exit(0); // Ensure clean exit on success
  } catch (err) {
    console.error('Error:', err);
    await anylist.teardown();
    process.exit(1);
  }
}

// Verify required environment variables
if (!process.env.EMAIL || !process.env.PASSWORD || !process.env.PRIMARY_LIST_NAME) {
  console.error('Missing required environment variables. Please check your .env file');
  process.exit(1);
}

displayActiveItems();
