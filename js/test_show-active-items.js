const dotenv = require('dotenv');
// Load environment variables from .test_env BEFORE other imports, and override any existing ones
dotenv.config({ path: './.test_env', override: true });

// Log environment variables to confirm they are loaded from .test_env
console.log(`DEBUG: EMAIL=${process.env.EMAIL}`);
console.log(`DEBUG: PASSWORD=${process.env.PASSWORD ? '******' : 'NOT SET'}`); // Avoid logging actual password
console.log(`DEBUG: PRIMARY_LIST_NAME=${process.env.PRIMARY_LIST_NAME}`);

const AnyList = require('anylist');
const fs = require('fs');

// Configure AnyList with credentials from environment

async function displayActiveItems() {
  const anylist = new AnyList({
    email: process.env.EMAIL,
    password: process.env.PASSWORD
  });
  try {
    await anylist.login();
    await anylist.getLists();

    const listName = process.env.PRIMARY_LIST_NAME;
    const list = anylist.getListByName(listName);

    if (!list) {
      console.error(`List "${listName}" not found`);
      if (anylist && typeof anylist.teardown === 'function') {
        anylist.teardown();
      }
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

    if (anylist && typeof anylist.teardown === 'function') {
      anylist.teardown();
    }
  } catch (err) {
    console.error('Error:', err);
    if (anylist && typeof anylist.teardown === 'function') {
      anylist.teardown();
    }
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