<template>
  <div class="dashboard">
    <RepoNav/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <div style="width: 80%; border: 1px solid #dfdfdf; padding: 10px 0 10px 10px; ">
      <b-row size="sm">
        <b-col cols="3">
          <span>base:</span>
          <b-form-select size="sm" v-model="base_branch" :options="base_branches"></b-form-select>
        </b-col>
        <b-col cols="3" offset="1">
          <span>compare:</span>
          <b-form-select size="sm" v-model="compare_branch" :options="compare_branches"></b-form-select>
        </b-col>
      </b-row>
    </div>

    <div v-for="d in diff" :key="d" style="width: 80%">
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button v-b-toggle="d[0]" variant="light">{{ d[0] }}</b-button>
        </b-card-header>
        <b-collapse :id="d[0]" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              <pre>{{ d[1] }}</pre>
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
    <div height="2em">&nbsp;</div>
    <b-card
      no-body
      v-for="l in log"
      :key="l"
      header="logInfo"
      header-tag="header"
      style="width: 80%"
    >
      <router-link :to="'/'+l.Author" slot="header" style="color: #656d74">
        <strong>{{ l.Author }}</strong>&nbsp;
      </router-link>
      <span slot="header">{{fromNowTime(l.Date)}}</span>
      <b-card-body>
        <p class="card-text">{{ l.message }}</p>
      </b-card-body>
    </b-card>
    <div height="2em">&nbsp;</div>
    <b-card style="width: 60%">
      <b-form @submit.prevent="onSubmit">
        <b-form-input v-model="title" placeholder="Title" required style="margin-bottom: 10px"></b-form-input>
        <b-form-textarea
          v-model="comment"
          placeholder="Leave a comment"
          size="md"
          rows="5"
          max-rows="10"
          style="margin-bottom: 10px"
        ></b-form-textarea>
        <b-button variant="success" type="submit" style="float: right">Submit Comment</b-button>
      </b-form>
    </b-card>
  </div>
</template>

<script>
import RepoNav from "@/components/RepoNav.vue";
import axios from "axios";
import moment from "moment";
// import MockAdapter from "axios-mock-adapter";
export default {
  data() {
    return {
      base_branch: "master",
      compare_branch: "master",
      base_branches: [],
      compare_branches: [],
      log: [],
      diff: [],
      title: "",
      comment: "",
      error: "",
      hasError: false
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData",
    base_branch: "next",
    compare_branch: "next"
  },
  methods: {
    fromNowTime(time) {
      return moment(time).fromNow();
    },
    fullCompareName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/compare";
    },
    next() {
      // console.log(1);
      if (this.base_owner == this.$route.params.owner) {
        this.$router.push(
          this.fullCompareName() +
            "/" +
            this.base_branch +
            "..." +
            this.compare_branch
        );
      } else {
        this.$router.push(
          this.fullCompareName() +
            "/" +
            this.base_owner +
            ":" +
            this.base_branch +
            "..." +
            this.compare_branch
        );
      }
    },
    fullRepoName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo;
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.$route.path).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   log: [
      //     {
      //       Author: "Bob",
      //       Date: "2019-04-17T11:20:29+08:00",
      //       message: "Merge Pull request"
      //     },
      //     {
      //       Author: "Alice",
      //       Date: "2019-04-16T20:12:00+0800",
      //       message: "Merge branch"
      //     }
      //   ],
      //   diff: [["a.vue", "x"], ["b.js", "y"]],
      //   base_owner: "Alice",
      //   base_branches: ["develop", "master"],
      //   compare_branches: ["develop", "master"]
      // });
      axios({
        method: "GET",
        url: this.$route.path,
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.log = response.data.log;
          this.diff = response.data.diff;
          this.base_owner = response.data.base_owner;
          this.base_branches = response.data.base_branches;
          this.compare_branches = response.data.compare_branches;
          this.next();
        } else {
          this.error = response.data.error;
          this.hasError = true;
        }
      });
    },
    onSubmit() {
      axios({
        method: "POST",
        url: this.$route.path,
        data: {
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          title: this.title,
          comment: this.comment
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.$router.push(
            "/" +
              response.data.owner +
              "/" +
              response.data.reponame +
              "/pull/" +
              response.data.id
          );
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
