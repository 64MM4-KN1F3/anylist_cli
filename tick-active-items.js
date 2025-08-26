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

// Verify required environment variables
if (!process.env.EMAIL || !process.env.PASSWORD || !process.env.PRIMARY_LIST_NAME) {
  console.error('Missing required environment variables (EMAIL, PASSWORD, PRIMARY_LIST_NAME). Please check your .env file.');
  process.exit(1);
}

async function tickActiveItems() {
  let itemsTicked = false;
  const tickedItemNames = [];
  const errorMessages = [];

  try {
    // Argument Parsing
    const args = process.argv.slice(2);
    if (args.length === 0 || args[0].trim() === '') {
      console.log("Usage: node tick-active-items.js <item_numbers>");
      console.log("Example: node tick-active-items.js 1,5,12");
      await anylist.teardown(); // Ensure teardown even on usage error
      process.exit(1);
    }

    const itemNumbersStr = args[0];
    const itemNumbers = itemNumbersStr.split(',').map(numStr => {
      const num = parseInt(numStr.trim(), 10);
      if (isNaN(num) || num <= 0) {
        errorMessages.push(`Warning: Invalid item number "${numStr}". Numbers must be positive integers.`);
        return null; // Mark as invalid
      }
      return num;
    }).filter(num => num !== null); // Filter out invalid entries

    if (itemNumbers.length === 0 && errorMessages.length > 0) {
        // Only invalid numbers were provided
        errorMessages.forEach(msg => console.error(msg));
        console.log("No valid item numbers provided.");
        await anylist.teardown();
        process.exit(1);
    }


    // AnyList Interaction
    await anylist.login();
    await anylist.getLists();

    const listName = process.env.PRIMARY_LIST_NAME;
    const list = anylist.getListByName(listName);

    if (!list) {
      console.error(`Error: List "${listName}" not found.`);
      await anylist.teardown();
      process.exit(1);
    }

    const activeItems = list.items.filter(item => !item.checked);

    // Ticking Items
    for (const itemNumber of itemNumbers) {
      const index = itemNumber - 1; // Adjust to zero-based index

      if (index >= 0 && index < activeItems.length) {
        const itemToTick = activeItems[index];
        if (!itemToTick.checked) {
            itemToTick.checked = true;
            await itemToTick.save(); // Save the individual item
            tickedItemNames.push(itemToTick.name);
            itemsTicked = true;
        } else {
            // This case should ideally not happen if we only fetch active items,
            // but good for robustness if logic changes or for direct manipulation.
            errorMessages.push(`Info: Item number ${itemNumber} ("${itemToTick.name}") was already checked.`);
        }
      } else {
        errorMessages.push(`Warning: Item number ${itemNumber} does not exist or is not active.`);
      }
    }


    // Output
    if (tickedItemNames.length > 0) {
      console.log(`List items ticked-off: ${tickedItemNames.join(', ')}`);
    } else if (errorMessages.length === 0) {
      console.log("No items were ticked off. Either no valid numbers provided or items already ticked.");
    }

    if (errorMessages.length > 0) {
      errorMessages.forEach(msg => console.warn(msg));
    }

    // Teardown and exit for successful completion
    await anylist.teardown();
    process.exit(0);
  } catch (err) {
    console.error('Error during script execution:', err.message);
    if (err.stack) {
        console.error(err.stack);
    }
    // Ensure teardown is called even if an error occurs mid-process
    await anylist.teardown();
    process.exit(1);
  } finally {
    // Teardown is now handled in try/catch before exit, so this can be removed or commented.
    // await anylist.teardown(); // No longer strictly needed here
  }
}

tickActiveItems();