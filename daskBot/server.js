const zerorpc = require("zerorpc");
const fs = require('fs');
const restify = require('restify');
const skype = require('skype-sdk');

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

const botService = new skype.BotService({
    messaging: {
        botId: '28:7a5eb625-40e0-4bef-a972-f2a11a7c9713',
        serverUrl : "https://apis.skype.com",
        requestTimeout : 15000,
        appId: '08a671a5-8713-470d-b37c-176e12e3e7b8',
        appSecret: 'H5sLkjSXDnL0gmGi2amUW10'
    }
});

botService.on('contactAdded', (bot, data) => {
    bot.reply(`Hello ${data.fromDisplayName}!`, true);
});

botService.on('personalMessage', (bot, data) => {
    client.invoke("command_callback", data.content, function(error, res, more) {
      console.log(res);
      if (res) {
        bot.reply(res, true);
      }
    });
});

botService.on('groupMessage', (bot, data) => {
    client.invoke("command_callback", data.content,  function(error, res, more) {
      console.log(res);
      if (res) {
        bot.reply(res, true);
      }
    });
});

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

const server = restify.createServer();
server.use(skype.verifySkypeCert())
server.post('/v1/chat', skype.messagingHandler(botService));
const port = process.env.PORT || 9000;
server.listen(port);
console.log('Listening for incoming requests on port ' + port);