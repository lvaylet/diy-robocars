<template>
  <div>
    <h1>{{ msg }}</h1>
    <button v-on:click="count++">You clicked me {{ count }} times.</button>
  </div>
</template>

<script>
import amqp from 'amqplib/callback_api';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data () {
    return {
      count: 0
    }
  },
  mounted () {
    amqp.connect('amqp://guest:guest@rabbitmq', function(err, conn) {
      if (err) {
        throw new Error(err)
      }

      console.log(conn)

      conn.createChannel(function(err, ch) {
        var q = 'pulse_width_microseconds';

        ch.assertQueue(q, {durable: false});

        console.log("Waiting for messages in %s. To exit press CTRL+C", q);
        ch.consume(q, function(msg) {
          console.log("Received %s", msg.content.toString());
        }, {noAck: true});
      });
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
