<template>
  <div class="reponav">
    <div class="bg-light" style="padding: 0 1%">
      <h4 style="padding:0.5rem 2%;">
        <router-link :to="'/'+$route.params.owner">{{$route.params.owner}}</router-link>
        <strong>/</strong>
        <router-link :to="'/'+fullRepoName()">{{ repoName() }}</router-link>
      </h4>
      <b-nav tabs>
        <b-nav-item
          :active="$route.name.match(/(Repo|PullCompare|FileContent)/)"
          :to="'/'+fullRepoName()"
        >Code</b-nav-item>
        <b-nav-item
          :active="$route.name.match(/Issues(List)?/)"
          :to="'/'+fullRepoName()+'/issues'"
        >Issues</b-nav-item>
        <b-nav-item
          :active="$route.name.match(/Pull(Request|RequestList|Conversion|Commits)/)"
          :to="'/'+fullRepoName()+'/pulls'"
        >Pull request</b-nav-item>
      </b-nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "Profile",
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  },
  methods: {
    fullRepoName() {
      return this.$route.params.owner + "/" + this.repoName();
    },
    repoName() {
      return this.$route.params.repo.split("/")[0];
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.reponav > :not(first-child) {
  margin-top: 1%;
}
</style>
