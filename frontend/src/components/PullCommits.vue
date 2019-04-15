<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <div>
      <span style="font-weight: 400; font-size: 32px;">{{ topic }}</span> &nbsp;
      <span
        style="font-weight: 300; font-size: 32px; color: #a3aab1"
      >#{{ $route.params.pullid }}</span>
      <div>
        <div v-if="pullState=='open'">
          <b-badge variant="success">Open</b-badge>
          <span>{{ pullUser }} wants to merge {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}</span>
        </div>
        <div v-else>
          <b-badge variant="info">Merged</b-badge>
          <span>{{ pullUser }} merged {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}</span>
        </div>
      </div>
    </div>

    <b-nav tabs>
      <b-nav-item :active="$route.name=='PullConversion'" :to="fullPullName()">Conversion</b-nav-item>
      <b-nav-item :active="$route.name=='PullCommits'" :to="fullPullName()+'/commits'">Commits</b-nav-item>
    </b-nav>

    <div v-for="reply in replys" :key="reply">
      <span>Commits on {{ reply.commitsDate }}</span>
      <div style="background-color: #f5fcff; margin-left: 1%; margin-top: 5px">
        <strong>{{ reply.title }}</strong>
        <p>{{ reply.user }} committed {{ reply.timeToNow }}</p>
      </div>
    </div>

    <p v-if="replys==''">no pull commits</p>
  </b-container>
</template>

<script>
import RepoNav from "@/components/RepoNav";
import axios from "axios";
// import MockAdapter from "axios-mock-adapter";
export default {
  data() {
    return {
      topic: "",
      pullState: "",
      pullUser: "",
      commitsNumber: "",
      pullTo: "",
      pullFrom: "",
      replys: ""
    };
  },
  beforeRouteEnter(to, from, next) {
    next(vm => vm.getData());
  },
  beforeRouteUpdate(to, from, next) {
    this.getData();
    next();
  },
  // created() {
  //   this.getData();
  // },
  // watch: {
  //   $route: "getData"
  // },
  methods: {
    fullPullName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/pull/" + param.pullid;
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullPullName() + "/commits").reply(200, {
      //   state: "ok",
      //   error: "error",
      //   topic: "a topic",
      //   pullState: "Merged",
      //   pullUser: "Alice",
      //   commitsNumber: 2,
      //   pullTo: "Alice:master",
      //   pullFrom: "Bob:abc",
      //   replys: {
      //     reply1: {
      //       commitsDate: "Apr 1, 2019",
      //       title: "a pull",
      //       user: "Alice",
      //       timeToNow: "8 das ago"
      //     }
      //   }
      // });
      axios({
        method: "GET",
        url: this.fullPullName() + "/commits",
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.pullid
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.topic = response.data.topic;
          this.pullState = response.data.pullState;
          this.pullUser = response.data.pullUser;
          this.commitsNumber = response.data.commitsNumber;
          this.pullTo = response.data.pullTo;
          this.pullFrom = response.data.pullFrom;
          this.replys = response.data.replys;
        } else {
          console.log(response.data.error);
        }
      });
    }
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
