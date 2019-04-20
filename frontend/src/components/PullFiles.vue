<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <div v-for="d in diff" :key="d" style="width: 80%">
      <b-button v-b-toggle="d[0]" variant="light">{{ d[0] }}</b-button>
      <b-collapse visible :id="d[0]">
        <b-card>{{ d[1] }}</b-card>
      </b-collapse>
    </div>
  </b-container>
</template>

<script>
import RepoNav from "@/components/RepoNav";
import axios from "axios";
import moment from "moment";
import MockAdapter from "axios-mock-adapter";
export default {
  data() {
    return {
      diff: []
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
      let mock = new MockAdapter(axios);
      mock.onGet(this.fullPullName()).reply(200, {
        state: "ok",
        error: "error",
        diff: [["a.vue", "x"], ["b.js", "y"]]
      });
      axios({
        method: "GET",
        url: this.fullPullName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.pullid
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.diff = response.data.diff;
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
