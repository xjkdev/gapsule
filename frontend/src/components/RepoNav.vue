<template>
  <div class="reponav">
    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <div class="bg-light" style="padding: 0 1%">
      <h4 style="padding:0.5rem 2%;">
        <router-link :to="'/'+$route.params.owner">{{$route.params.owner}}</router-link>
        <strong>/</strong>
        <router-link :to="'/'+fullRepoName()">{{ repoName() }}</router-link>
        <b-button variant="outline-info" @click="fork" class="fork" v-if="showFork">fork</b-button>
      </h4>
      <b-nav tabs>
        <b-nav-item :active="$route.name.match(/(Repo|FileContent)/)" :to="'/'+fullRepoName()">Code</b-nav-item>
        <b-nav-item
          :active="$route.name.match(/Issues(List)?/)"
          :to="'/'+fullRepoName()+'/issues'"
        >Issues</b-nav-item>
        <b-nav-item
          :active="$route.name.match(/Pull(Compare|Request|RequestList|Conversion|Commits|Files)/)"
          :to="'/'+fullRepoName()+'/pulls'"
        >Pull request</b-nav-item>
      </b-nav>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getCookie } from "@/utils/get_cookie";
export default {
  name: "Profile",
  data() {
    return {
      msg: "Welcome to Your Vue.js App",
      error: "",
      showFork: false,
      hasError: false
    };
  },
  created() {
    this.$router.afterEach((to, _from) => {
      this.showFork = to.name == "Repo";
    });
    this.showFork = this.$route.name == "Repo";
  },
  methods: {
    fullRepoName() {
      return this.$route.params.owner + "/" + this.repoName();
    },
    repoName() {
      return this.$route.params.repo.split("/")[0];
    },
    fork() {
      let current_user = getCookie("username");
      if (current_user == null) {
        this.$router.push(
          "/signin?next=" + encodeURIComponent(this.$router.fullPath)
        );
      } else {
        axios({
          method: "POST",
          url: "/" + this.fullRepoName(),
          data: {
            action: "fork"
          }
        }).then(response => {
          if (response.status == 200 && response.data.state == "ok") {
            console.log(this.repoName());
            this.$router.push("/" + current_user + "/" + this.repoName());
          } else {
            this.error = response.data.error;
            this.hasError = true;
          }
        });
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.reponav > :not(first-child) {
  margin-top: 1%;
}
.fork {
  float: right;
}
</style>
