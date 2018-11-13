<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <RabbitMQConsumer msg="Simple Boilerplate"/>
  </div>
</template>

<script>
import RabbitMQConsumer from './components/RabbitMQConsumer.vue'

export default {
  name: 'app',
  components: {
    RabbitMQConsumer
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
