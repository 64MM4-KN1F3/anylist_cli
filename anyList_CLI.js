const AnyList = require('anylist');
const readline = require('readline');
const dotenv = require('dotenv');

// Load the environment variables from the .env file
dotenv.config();

// Replace with your actual email and password
const email = process.env.EMAIL;
const password = process.env.PASSWORD;
const sharedGroceryListName = 'Shared Grocery List'
const sharedGroceryListId = 'f9c5a71651c147e5814ea2068f4bf28d';


const anylist = new AnyList({ email, password });

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const handleError = (err) => {
  console.error('Error:', err);
  process.exit(1);
};

/*
const promptListName = () => {
  return new Promise((resolve) => {
    rl.question('Enter the list name: ', (listName) => {
      resolve(listName);
    });
  });
};
*/

const promptItemName = () => {
  return new Promise((resolve) => {
    rl.question('Enter the item name: ', (itemName) => {
      resolve(itemName);
    });
  });
};

const addItemToList = async (listName, itemName) => {
  try {
    await anylist.login();
    await anylist.getLists();

    const list = anylist.getListByName(listName);
    //const list = anylist.getListById(sharedGroceryListId);

    if (!list) {
      console.error(`List "${listName}", with id, "${sharedGroceryListId}" not found.`);
      return;
    }

    const existingItem = list.getItemByName(itemName);
    if (existingItem) {
      console.log(`Item "${itemName}" already exists in "${listName}".`);
      return;
    }

    const newItem = anylist.createItem({ name: itemName });
    const addedItem = await list.addItem(newItem);
    console.log(`Item "${addedItem.name}" added to "${listName}".`);

    anylist.teardown();
  } catch (err) {
    handleError(err);
  }
};

const main = async () => {
    let shouldExit = false;
  
    while (!shouldExit) {
      const itemName = await promptItemName();
  
      if (itemName.toLowerCase() === 'exit') {
        shouldExit = true;
      } 
      if (itemName.toLowerCase() === 'quit') {
        shouldExit = true;
      } else {
        await addItemToList(sharedGroceryListName, itemName);
      }
    }
  
    anylist.teardown();
    rl.close();
    process.exit(0); // Exit the script
  };

main();