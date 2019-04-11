<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <div>
      <span style="font-weight: 400; font-size: 32px;">{{ topic }}</span> &nbsp;
      <span
        style="font-weight: 300; font-size: 32px; color: #a3aab1"
      >#{{ $route.params.pullid }}</span>

      <div>
        <p v-if="pullState=='open'">
          <b-badge variant="success">Open</b-badge>
          {{ pullUser }} wants to merge {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}
        </p>
        <p v-else>
          <b-badge variant="info">Merged</b-badge>
          {{ pullUser }} merged asdfaadsfa {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}
        </p>
      </div>
    </div>

    <b-nav tabs>
      <b-nav-item :active="$route.name=='PullConversion'" :to="fullPullName()">Conversion</b-nav-item>
      <b-nav-item :active="$route.name=='PullCommits'" :to="fullPullName()+'/commits'">Commits</b-nav-item>
    </b-nav>

    <b-card
      no-body
      v-for="reply in replys"
      :key="reply"
      header="commetInfo"
      header-tag="header"
      style="width: 60%"
    >
      <router-link :to="'/'+reply.user" slot="header" style="color: #656d74">
        <strong>{{ reply.user }}</strong>&nbsp;
      </router-link>
      <span slot="header">commented {{reply.date}}</span>
      <b-card-body>
        <p class="card-text">{{ reply.text }}</p>
      </b-card-body>
    </b-card>

    <b-card style="width: 60%">
      <b-form>
        <b-form-textarea
          v-model="comments"
          placeholder="Leave a commet"
          size="md"
          rows="5"
          max-rows="10"
          style="margin-bottom: 10px"
        ></b-form-textarea>
        <div style="float: right">
          <b-button variant="success" type="submit" @click.prevent="comment">Comment</b-button>
        </div>
      </b-form>
    </b-card>
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
      replys: [],
      comments: ""
    };
  },
  // beforeRouteEnter(to, from, next) {
  //   console.log("x");
  //   next(vm => vm.getData());
  // },
  // beforeRouteUpdate(to, from, next) {
  //   this.getData();
  //   next();
  // },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    fullPullName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/pull/" + param.pullid;
    },
    comment() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullPullName()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   user: "Mike"
      // });
      axios({
        method: "GET",
        url: this.fullPullName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.pullid,
          comments: this.comments
        }
      }).then(response => {
        if (response.data.state == "ok") {
          let tmp = {};
          tmp["user"] = response.data.user;
          tmp["date"] = "just now";
          tmp["text"] = this.comments;
          this.replys.push(tmp);
          this.comments = "";
        } else {
          console.log(response.data.error);
        }
      });
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullPullName()).reply(200, {
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
      //       user: "Alice",
      //       date: "1 day ago",
      //       text: "a reply text"
      //     },
      //     reply2: {
      //       user: "Bob",
      //       date: "2 days ago",
      //       text: "another reply text"
      //     }
      //   }
      // });
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
          this.topic = response.data.topic;
          this.pullState = response.data.pullState;
          this.pullUser = response.data.pullUser;
          this.commitsNumber = response.data.commitsNumber;
          this.pullTo = response.data.pullTo;
          this.pullFrom = response.data.pullFrom;
          let replyData;
          for (replyData in response.data.replys) {
            this.replys.push(response.data.replys[replyData]);
          }
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
