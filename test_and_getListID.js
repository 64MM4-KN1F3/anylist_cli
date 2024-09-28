const AnyList = require('anylist');
const dotenv = require('dotenv');

const any = new AnyList({email: process.env.EMAIL, password: process.env.PASSWORD});

any.login().then(async () => {
    var myLists = await any.getLists();
    
    console.log(myLists)
});
