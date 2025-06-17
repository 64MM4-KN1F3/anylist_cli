const AnyList = require('anylist'); // https://github.com/codetheweb/anylist/blob/master/README.md
const readline = require('readline');
const dotenv = require('dotenv');
const fs = require('fs');

// Load environment variables from .test_env
dotenv.config({ path: './.test_env' });

// Function to ensure .env file exists and load environment variables
const initEnvFile = () => {
  const envFilePath = '.env'; // .env is assumed to be in the same directory
  if (!fs.existsSync(envFilePath)) {
    console.log('.env file not found, creating a new one...');
    fs.writeFileSync(envFilePath, ''); // create an empty .env file
  }
  dotenv.config({ path: envFilePath }); // load environment variables
};

// Function to update .env file
const updateEnvFile = (key, value) => {
  const envFilePath = '.env'; // .env is assumed to be in the same directory
  let envConfig = fs.readFileSync(envFilePath, 'utf8');
  const regex = new RegExp(`^${key}=.*`, 'm');

  if (envConfig.match(regex)) {
    envConfig = envConfig.replace(regex, `${key}=${value}`);
  } else {
    envConfig += `\n${key}=${value}`;
  }

  fs.writeFileSync(envFilePath, envConfig);
};

// Load the environment variables from the .env file
initEnvFile();

// Pull .env vars
let email = process.env.EMAIL;
let password = process.env.PASSWORD;
let sharedGroceryListName = process.env.PRIMARY_LIST_NAME;

// Function to prompt user for input
const promptUser = (question) => {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
};

// Check env variables
const checkEnvVariables = async () => {
  console.log('email: %s', email);
  if (!email) {
    email = await promptUser('Enter your email: ');
    updateEnvFile('EMAIL', email);
  }

  if (!password) {
    password = await promptUser('Enter your password: ');
    updateEnvFile('PASSWORD', password);
  }

  if (!sharedGroceryListName) {
    sharedGroceryListName = await promptUser('Enter the primary grocery list name: ');
    updateEnvFile('PRIMARY_LIST_NAME', sharedGroceryListName);
  }
};


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

    if (!list) {
      console.error(`List "${listName}", with id, "${sharedGroceryListId}" not found.`);
      return;
    }

    const existingItem = list.getItemByName(itemName);
    if (existingItem) {
      if (existingItem.checked) {
        existingItem.checked = false;
        await existingItem.save();
        console.log(`Item "${itemName}" readded to "${listName}".`);
      }
      else {
        console.log(`Item "${itemName}" already exists in "${listName}".`);
      }
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
    await checkEnvVariables();

    let shouldExit = false;
  
    while (!shouldExit) {
      const itemName = await promptItemName();
  
      if (['exit', 'quit', 'q'].includes(itemName.toLowerCase())) {
        shouldExit = true;
      } else if ([''].includes(itemName.toLowerCase())){
        // Do nothing
      } else {
        await addItemToList(sharedGroceryListName, itemName);
      }
    }
  
    anylist.teardown();
    rl.close();
    process.exit(0); // Exit the script
  };

main();