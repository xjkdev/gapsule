<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <b-row>
      <b-col cols="4">
        <b-form-input v-if="isIssuePage" placeholder="Search Issues" @keyup.enter="getSearchDatas"></b-form-input>
        <b-form-input v-else placeholder="Search Pulls" @keyup.enter="getSearchDatas"></b-form-input>
      </b-col>
      <b-col cols="2" offset="6">
        <b-button block variant="success" @click="newIssue">New {{ operateType }}</b-button>
      </b-col>
    </b-row>

    <b-card no-body v-for="issue in issues" :key="issue">
      <b-card-body>
        <router-link :to="fullIssuesName()+'/'+issue.post_id">
          <h5 class="card-title">{{ issue.title }}</h5>
        </router-link>
        <p
          class="card-text"
        >{{'#'+issue.post_id+' opened on '+fromNowTime(issue.post_time)+' by '+issue.postername}}</p>
      </b-card-body>
    </b-card>

    <b-card no-body v-if="issues==''">
      <b-card-body v-if="isIssuePage">no issues</b-card-body>
      <b-card-body v-else>no pulls</b-card-body>
    </b-card>
  </b-container>
</template>

<script>
import RepoNav from "@/components/RepoNav";
import axios from "axios";
import moment from "moment";
// import MockAdapter from "axios-mock-adapter";
export default {
  props: {
    operateType: {
      // type: String
      validator: function(value) {
        return ["issues", "pull"].indexOf(value) !== -1;
      }
    }
  },
  data() {
    return {
      issues: "",
      error: "",
      hasError: false
    };
  },
  created() {
    this.getIssues();
  },
  watch: {
    $route: "getIssues"
  },
  methods: {
    fullIssuesName() {
      let param = this.$route.params;
      if (this.operateType == "issues") {
        return "/" + param.owner + "/" + param.repo + "/issues";
      } else {
        return "/" + param.owner + "/" + param.repo + "/pulls";
      }
    },
    fromNowTime(time) {
      return moment(time).fromNow();
    },
    getIssues() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullIssuesName()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   issues: [
      //     {
      //       title: "a topic",
      //       post_id: "11",
      //       post_time: "2019-04-17T11:20:29+08:00",
      //       postername: "Alice"
      //     },
      //     {
      //       title: "another topic",
      //       post_id: "12",
      //       post_time: "2019-04-16T20:12:00+0800",
      //       postername: "Bob"
      //     }
      //   ]
      // });
      axios({
        method: "GET",
        url: this.fullIssuesName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.issues = response.data.issues;
        } else {
          this.error = response.data.error;
          this.hasError = true;
        }
      });
    },
    getSearchDatas() {
      this.getIssues();
    },
    newIssue() {
      if (this.operateType == "issues") {
        this.$router.push(this.fullIssuesName() + "/new");
      } else {
        let param = this.$route.params;
        this.$router.push("/" + param.owner + "/" + param.repo + "/compare");
      }
    }
  },
  computed: {
    isIssuePage() {
      return this.operateType == "issues";
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

a {
  text-decoration: none;
  color: #222;
}
a:hover {
  text-decoration: none;
  color: #0366d9;
}
</style>
