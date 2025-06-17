const AnyList = require('anylist');
const dotenv = require('dotenv');
const fs = require('fs');



// Load environment variables from .test_env
dotenv.config({ path: './.test_env' });

// Configure AnyList with credentials from environment
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
      anylist.teardown();
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

    anylist.teardown();
  } catch (err) {
    console.error('Error:', err);
    anylist.teardown();
    process.exit(1);
  }
}

// Verify required environment variables
if (!process.env.EMAIL || !process.env.PASSWORD || !process.env.PRIMARY_LIST_NAME) {
  // Updated error message for clarity
  console.error('Missing required environment variables. Please check your specified .env file');
  process.exit(1);
}

displayActiveItems();