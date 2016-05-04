'use strict';

const Pusher = require('pusher-client');
const request = require('superagent');
const restify = require('restify');
const skype = require('skype-sdk');

const CommandProcessor = require('./command-processor');
const config = require('./config');

const botService = new skype.BotService({
    messaging: {
        botId: config.BOT_ID,
        serverUrl : "https://apis.skype.com",
        requestTimeout : 15000,
        appId: config.APP_ID,
        appSecret: config.APP_SECRET,
    }
});

botService.on('contactAdded', (bot, data) => {
    bot.reply(`Hello ${data.fromDisplayName}! I am Daskbot 2.0`, true);
});

function processCommand(data, successHandler, errorHandler) {
  if (data.content.startsWith('%')) {
    CommandProcessor.handleCommand(data, successHandler, errorHandler);
  }
  else {
    // Sentiment anaysis service. Uses https://market.mashape.com/vivekn/sentiment-3
    request
    .post('https://community-sentiment.p.mashape.com/text/')
    .set('X-Mashape-Key', config.MASHAPE_KEY)
    .send( `txt=${data.content}`)
    .end(function(err, res) {
      if (!err) {
        if (parseInt(res.body.result.confidence) >= 75 && res.body.result.sentiment === 'Negative') {
          successHandler(`Hey ${data.from}, Are you angry/sad? (confidence ${res.body.result.confidence})`);
        }
        else if (parseInt(res.body.result.confidence) >= 75 && res.body.result.sentiment === 'Positive') {
          successHandler(`Hey ${data.from}, Why are you so positive? (confidence ${res.body.result.confidence})`);
        }
      }
    })
  }
}

function handleMessage(bot, data) {
  processCommand(data,
    function(res) {
      bot.reply(" >> " + res);
    },
    function(err) {
      bot.reply(" >> " + err);
    }
  );
}

botService.on('personalMessage', (bot, data) => {
  handleMessage(bot, data);
});

botService.on('groupMessage', (bot, data) => {
  handleMessage(bot, data);
});

const pusher = new Pusher(config.PUSHER_KEY, {
  encrypted: true
});

const channelMotd = pusher.subscribe('motd');
const channelStreamer = pusher.subscribe('streamer');

function broadcastSkype(successMessage, errorMessage) {
  request
  .get(config.API_ENDPOINT + 'skype')
  .end(function(err, res) {
    if (!err) {
      const result = res.body.result;
      for (let i = 0; i < result.length; i++) {
        botService.send(result[i], successMessage);
      }
    }
    else {
      console.log(errorMessage);
    }
  });
}

channelMotd.bind('motd_update', function(data) {
  broadcastSkype(` >> Today's message is: ${data.result.message}`,
                 'Error on grabbing list of subscribers. [motd_update]');
});

channelStreamer.bind('streamer_added', function(data) {
  broadcastSkype(` >> ${data.result_added.display_name} added to streamer list!`,
                 'Error on grabbing list of subscribers. [streamer_online]');
})
.bind('streamer_removed', function(data) {
  broadcastSkype(` >> ${data.result_removed.display_name} removed from streamer list!`,
                 'Error on grabbing list of subscribers. [streamer_online]');
})
.bind('streamer_online', function(data) {
  broadcastSkype(` >> ${data.result.display_name} is online! - https://www.twitch.tv/${data.result.name}`,
                 'Error on grabbing list of subscribers. [streamer_online]');
})
.bind('streamer_offline', function(data) {
  broadcastSkype(` >> ${data.result.display_name} went offline.`,
                 'Error on grabbing list of subscribers. [streamer_offline]');
});

const server = restify.createServer();
server.use(skype.verifySkypeCert())
server.post('/v1/chat', skype.messagingHandler(botService));
const port = process.env.PORT || 9000;
server.listen(port);
console.log('Listening for incoming requests on port ' + port);
