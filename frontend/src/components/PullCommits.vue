<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <div>
      <span style="font-weight: 400; font-size: 32px;">{{ title }}</span> &nbsp;
      <span
        style="font-weight: 300; font-size: 32px; color: #a3aab1"
      >#{{ $route.params.pullid }}</span>
      <div>
        <div v-if="status=='Open'">
          <b-badge variant="success">Open</b-badge>
          <span>{{ pullUser }} wants to merge {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}</span>
        </div>
        <!-- FIXME: 这里差了 Closed -->
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
      title: "",
      status: "",
      pullUser: "",
      commitsNumber: "",
      pullTo: "",
      pullFrom: "",
      replys: "",
      error: "",
      hasError: false
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
      //   title: "a title",
      //   status: "Merged",
      //   pullUser: "Alice",
      //   commitsNumber: 2,
      //   pullTo: "Alice:master",
      //   pullFrom: "Bob:abc",
      //   replys: [
      //     {
      //       commitsDate: "Apr 1, 2019",
      //       title: "a pull",
      //       user: "Alice",
      //       timeToNow: "8 das ago"
      //     }
      //   ]
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
          this.title = response.data.title;
          this.status = response.data.status;
          this.pullUser = response.data.pullUser;
          this.commitsNumber = response.data.commitsNumber;
          this.pullTo = response.data.pullTo;
          this.pullFrom = response.data.pullFrom;
          this.replys = response.data.replys;
        } else {
          this.error = response.data.error;
          this.hasError = true;
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
