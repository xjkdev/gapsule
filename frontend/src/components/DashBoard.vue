<template>
  <div class="dashboard">
    <p>dashboard</p>
    <b-card title="Message 1">
      <b-card-text>Some quick example text to build on the card title and make up the bulk of the card's content.</b-card-text>
    </b-card>
    <b-card title="Message 2">
      <b-card-text>Some quick example text to build on the card title and make up the bulk of the card's content.</b-card-text>
    </b-card>
    <b-card title="Message 3">
      <b-card-text>Some quick example text to build on the card title and make up the bulk of the card's content.</b-card-text>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "DashBoard",
  data() {
    return {};
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard > :not(first-child) {
  margin-top: 1%;
}
</style>
