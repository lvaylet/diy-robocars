// This works in standalone mode (i.e. with `node consume.js`) but not
// in a vue.js frontend app:
//
//   var amqp = require('amqplib/callback_api');
//
// This link recommends using `import` instead:
// https://stackoverflow.com/questions/33683539/webpack-require-is-not-a-function-when-using-babel-6
//
//   import amqp from 'amqplib/callback_api';
//
// But same result. This link highlights that "you can"t use server-side
// code, like amqplib, in a browser.":
// https://stackoverflow.com/questions/45936495/uncaught-typeerror-webpack-require-connect-is-not-a-function-at-connec

var amqp = require('amqplib/callback_api');

amqp.connect('amqp://guest:guest@localhost', function(err, conn) {
  if (err) { throw new Error(err) };

  conn.createChannel(function(err, ch) {
    if (err) { throw new Error(err) };

    var q = 'pulse_width_microseconds';

    ch.assertQueue(q, {durable: false});

    console.log("Waiting for messages in %s. To exit press CTRL+C", q);
    ch.consume(q, function(msg) {
      console.log("Received %s", msg.content.toString());
    }, {noAck: true});
  });
});
