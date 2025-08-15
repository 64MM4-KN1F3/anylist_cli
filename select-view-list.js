const AnyList = require('anylist');
const readline = require('readline');
const dotenv = require('dotenv');

// Load environment variables from .env
dotenv.config();

const anylist = new AnyList({
  email: process.env.EMAIL,
  password: process.env.PASSWORD
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const main = async () => {
  try {
    await anylist.login();
    await anylist.getLists();

    const lists = anylist.lists;
    console.log('Available lists:');
    lists.forEach((list, index) => {
      console.log(`${index + 1}. ${list.name}`);
    });

    const listIndex = await new Promise(resolve => {
      rl.question('Select a list to view (enter the number): ', answer => {
        resolve(parseInt(answer, 10) - 1);
      });
    });

    if (isNaN(listIndex) || listIndex < 0 || listIndex >= lists.length) {
      console.error('Invalid selection.');
      rl.close();
      await anylist.teardown();
      return;
    }

    const selectedList = lists[listIndex];
    console.log(`\nItems in "${selectedList.name}":`);
    if (selectedList.items.length === 0) {
      console.log('No items in this list.');
    } else {
      selectedList.items.forEach(item => {
        console.log(`- ${item.name} ${item.checked ? '(checked)' : ''}`);
      });
    }

    rl.close();
    await anylist.teardown();
  } catch (error) {
    console.error('An error occurred:', error);
    rl.close();
    await anylist.teardown();
  }
};

main();