<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>
    <b-card no-body>
      <b-card-body>
        <h5 class="card-title">Title</h5>
        <p
          class="card-text"
        >Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      </b-card-body>
    </b-card>
    <b-card no-body>
      <b-card-body>
        <h5 class="card-title">Reply 1</h5>
        <p
          class="card-text"
        >Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      </b-card-body>
    </b-card>
    <b-card no-body>
      <b-card-body>
        <h5 class="card-title">Reply 2</h5>
        <p
          class="card-text"
        >Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      </b-card-body>
    </b-card>
  </b-container>
</template>

<script>
import RepoNav from "@/components/RepoNav";
export default {
  name: "Profile",
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  },
  components: { RepoNav }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard > :not(first-child) {
  margin-top: 1%;
}
</style>
