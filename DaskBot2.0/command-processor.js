'use strict';

const request = require('superagent');
const config = require('./config');

const commandTable = {
  '%subscribe': function(args, data, successHandler, errorHandler) {
    const chat_id = config.BOT_ID === data.to ? data.from : data.to;
    request
    .post(config.API_ENDPOINT + 'skype')
    .send({ submitted_by: data.from, chatid: chat_id })
    .end(function(err, res) {
      if (!err) {
        successHandler(`${chat_id} subscribed!`);
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%unsubscribe': function(args, data, successHandler, errorHandler) {
    const chat_id = config.BOT_ID === data.to ? data.from : data.to;
    request
    .del(config.API_ENDPOINT + 'skype')
    .send({ chatid: chat_id })
    .end(function(err, res) {
      if (!err) {
        successHandler(`${chat_id} unsubscribed.`);
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%8ball': function(args, data, successHandler, errorHandler) {
    request
    .get(config.API_ENDPOINT + 'eight_ball')
    .end(function(err, res) {
      if (!err) {
        successHandler(`${res.body.result.answer}. [${res.body.result.status}]`);
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%message': function(args, data, successHandler, errorHandler) {
    if (!args.length) {
      request
      .get(config.API_ENDPOINT + 'motd')
      .end(function(err, res) {
        if (!err) {
          successHandler(`Today's message is: ${res.body.result.message}`);
        }
        else {
          errorHandler(`Error: ${err.response.body.error}`);
        }
      });
    }
    else {
      request
      .patch(config.API_ENDPOINT + 'motd')
      .send({ submitted_by: data.from, message: args.join(" ") })
      .end(function(err, res) {
        if (!err) {
          // Broadcast should happen
        }
        else {
          errorHandler(`Error: ${err.response.body.error}`);
        }
      });
    }
  },
  '%live': function(args, data, successHandler, errorHandler) {
    request
    .get(config.API_ENDPOINT + 'streamer/get-live')
    .end(function(err, res) {
      if (!err) {
        let result = '';
        for (let i = 0; i < res.body.result.length; i++) {
          let currentStreamer = res.body.result[i]
          result += `${currentStreamer.stream.channel.display_name} (Viewers: ${currentStreamer.stream.viewers}) - ${currentStreamer.stream.channel.url} \n`;
        }
        successHandler(result);
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%streamers': function(args, data, successHandler, errorHandler) {
    request
    .get(config.API_ENDPOINT + 'streamer')
    .end(function(err, res) {
      if (!err) {
        successHandler(res.body.result.sort().join(", "));
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%addstreamer': function(args, data, successHandler, errorHandler) {
    request
    .post(config.API_ENDPOINT + 'streamer')
    .send({ submitted_by: data.from, id: args[0] })
    .end(function(err, res) {
      if (!err) {
        // Broadcast should happen
        // successHandler(`${res.body.result.display_name} subscribed!`);
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%removestreamer': function(args, data, successHandler, errorHandler) {
    request
    .del(config.API_ENDPOINT + 'streamer')
    .send({ submitted_by: data.from, id: args[0] })
    .end(function(err, res) {
      if (!err) {
        // Broadcast should happen
        // successHandler(`${res.body.result.display_name} subscribed!`);
      }
      else {
        errorHandler(`Error: ${err.response.body.error}`);
      }
    });
  },
  '%help': function(args, data, successHandler, errorHandler) {
    successHandler(`List of commands:\n${Object.keys(commandTable).sort().join("\n")}`);
  },
  '%csgo': function(args, data, successHandler, errorHandler) {
    successHandler('<b>GOGOGOGOGOGGO\nGOGOGOGOGOGGO\nGOGOGOGOGOGGO\nGOGOGOGOGOGGO\n</b>');
  },
  '%kawkaw': function(args, data, successHandler, errorHandler) {
    successHandler('<b>KAW AWH KAW AWH KAW AWH\nKAW AWH KAW AWH KAW AWH\nKAW AWH KAW AWH KAW AWH\nKAW AWH KAW AWH KAW AWH\n</b>');
  },
  '%wubwub': function(args, data, successHandler, errorHandler) {
    successHandler('<i>WUBWUBWUBWUB\nWUBWUBWUBWUB\nWUBWUBWUBWUB\nWUBWUBWUBWUB\n</i>');
  },
  '%watchtogether': function(args, data, successHandler, errorHandler) {
    successHandler('https://instasync.com/r/Windask');
  },
  '%theclub': function(args, data, successHandler, errorHandler) {
    successHandler('http://www.soulwalrus.club');
  },
  '%bot-train-t': function(args, data, successHandler, errorHandler) {
    successHandler('\nchangelevel de_dust2\nmp_autoteambalance 0;\nmp_limitteams 0;\nmp_maxrounds 100;\n' +
                   'bot_kick;\nbot_add_ct;\nbot_add_ct;\nbot_add_ct;\nbot_add_ct;\nbot_add_ct;\nbot_add_ct;\n' +
                   'bot_add_ct;\nbot_add_ct;\nbot_add_ct; \nbot_add_ct;\nbot_difficulty 3;');
  },
  '%bot-train-ct': function(args, data, successHandler, errorHandler) {
    successHandler('\nchangelevel de_dust2\nmp_autoteambalance 0;\nmp_limitteams 0;\nmp_maxrounds 100;\n' +
                   'bot_kick;\nbot_add_t;\nbot_add_t;\nbot_add_t;\nbot_add_t;\nbot_add_t;\nbot_add_t;\n' +
                   'bot_add_t;\nbot_add_t;\nbot_add_t; \nbot_add_t;\nbot_difficulty 3;');
  },
}

module.exports = {
  handleCommand: function(data, successHandler, errorHandler) {
    const parsed = data.content.trim().split(/\s+/);
    const command = parsed[0];
    const args = parsed.splice(1);
    if (commandTable[command]) {
      commandTable[command](args, data, successHandler, errorHandler);
    }
    else {
      errorHandler(`Command <b>${command}</b> not supported. Send suggestions at ryan@soulwalrus.club. \n <b>%help</b> for commands.`)
    }
  }
};
