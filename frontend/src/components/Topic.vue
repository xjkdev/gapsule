<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <div>
      <span style="font-weight: 400; font-size: 32px;">{{ title }}</span> &nbsp;
      <span
        style="font-weight: 300; font-size: 32px; color: #a3aab1"
      >#{{ $route.params.issueid }}</span>
      <p>
        <b-badge v-if="isOpen" variant="success" disabled size="sm">Opened</b-badge>
        <b-badge v-else variant="danger" disabled size="sm">Closed</b-badge>
        &nbsp;
        {{ poster }} opened this issue {{ date }} · {{ commetsNumber }} comments
      </p>
    </div>

    <b-card
      no-body
      v-for="reply in replys"
      :key="reply"
      header="commetInfo"
      header-tag="header"
      style="width: 60%"
    >
      <router-link :to="'/'+reply.commenter" slot="header" style="color: #656d74">
        <strong>{{ reply.commenter }}</strong>&nbsp;
      </router-link>
      <span slot="header">commented {{reply.address_time}}</span>
      <b-card-body>
        <p class="card-text">{{ reply.content }}</p>
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
          <template v-if="show">
            <b-button v-if="isOpen" type="submit" @click.prevent="closeIssue">Close Issue</b-button>
            <b-button v-else type="submit" @click.prevent="reopenIssue">Reopen Issue</b-button>
          </template>
          <b-button
            variant="success"
            type="submit"
            style="margin-left: 5px"
            @click.prevent="comment"
          >Comment</b-button>
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
      title: "",
      poster: "",
      date: "",
      commetsNumber: "",
      replys: [],
      comments: "",
      show: true,
      isOpen: true
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    fullIssueName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/issues/" + param.issueid;
    },
    closeIssue() {
      this.isOpen = false;
      axios({
        method: "GET",
        url: this.fullIssueName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.issueid,
          action: "closeIssue"
        }
      }).then(response => {
        if (response.data.state == "ok") {
          console.log("this issue is closed");
        } else {
          console.log(response.data.error);
        }
      });
    },
    reopenIssue() {
      this.isOpen = true;
      axios({
        method: "GET",
        url: this.fullIssueName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.issueid,
          action: "reopenIssue"
        }
      }).then(response => {
        if (response.data.state == "ok") {
          console.log("this issue is opend");
        } else {
          console.log(response.data.error);
        }
      });
    },
    comment() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullIssueName()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   commenter: "C"
      // });
      axios({
        method: "GET",
        url: this.fullIssueName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.issueid,
          comments: this.comments
        }
      }).then(response => {
        if (response.data.state == "ok") {
          let tmp = {};
          tmp["commenter"] = response.data.poster;
          tmp["address_time"] = "just now";
          tmp["content"] = this.comments;
          this.replys.push(tmp);
          this.comments = "";
        } else {
          console.log(response.data.error);
        }
      });
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullIssueName()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   title: "a title",
      //   poster: "Alice",
      //   comments: [
      //     {
      //       commenter: "Alice",
      //       address_time: "1 day ago",
      //       content: "a reply text"
      //     },
      //     {
      //       commenter: "Bob",
      //       address_time: "2 days ago",
      //       content: "another reply text"
      //     }
      //   ],
      //   show: true,
      //   isOpen: true
      // });
      axios({
        method: "GET",
        url: this.fullIssueName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          id: this.$route.params.issueid
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.title = response.data.title;
          this.poster = response.data.poster;
          this.date = response.data.comments[0].address_time;
          this.commetsNumber = response.data.comments.length;
          this.show = response.data.show;
          this.isOpen = response.data.isOpen;
          let replyData;
          for (replyData in response.data.comments) {
            this.replys.push(response.data.comments[replyData]);
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
