const AnyList = require('anylist');
const dotenv = require('dotenv');

// Load environment variables
if (process.env.NODE_ENV === 'test') {
  dotenv.config({ path: '.test_env' });
} else {
  dotenv.config();
}

// Configure AnyList with credentials from .env
const anylist = new AnyList({
  email: process.env.EMAIL,
  password: process.env.PASSWORD
});

function parseUpdateArgs(args) {
    if (args.length < 2) {
        throw new Error("Invalid arguments. Usage: -u <item_number> <new_item_name>");
    }

    const itemNumber = parseInt(args, 10);
    if (isNaN(itemNumber) || itemNumber <= 0) {
        throw new Error("Invalid item number. Must be a positive integer.");
    }

    const newItemName = args.slice(1).join(' ');

    return [{ index: itemNumber, name: newItemName }];
}


async function updateItems(updates) {
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

    for (const update of updates) {
        const { index, name } = update;
        if (index > 0 && index <= activeItems.length) {
            const itemToUpdate = activeItems[index - 1];
            console.log(`Updating item ${index} ("${itemToUpdate.name}") to "${name}"`);
            itemToUpdate.name = name;
            await itemToUpdate.save();
            console.log(`Item ${index} updated successfully.`);
        } else {
            console.error(`Invalid item number: ${index}. There are only ${activeItems.length} active items.`);
        }
    }

    await anylist.teardown();
    process.exit(0);
  } catch (err) {
    console.error('Error:', err);
    await anylist.teardown();
    process.exit(1);
  }
}

if (!process.env.EMAIL || !process.env.PASSWORD || !process.env.PRIMARY_LIST_NAME) {
  console.error('Missing required environment variables. Please check your .env file');
  process.exit(1);
}

const args = process.argv.slice(2);
try {
    const updates = parseUpdateArgs(args);
    if (updates.length > 0) {
        updateItems(updates);
    } else {
        console.log("No update commands provided.");
    }
} catch (e) {
    console.error("Error parsing arguments:", e.message);
    process.exit(1);
}