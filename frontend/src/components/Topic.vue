<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <div>
      <span style="font-weight: 400; font-size: 32px;">{{ title }}</span> &nbsp;
      <span
        style="font-weight: 300; font-size: 32px; color: #a3aab1"
      >#{{ $route.params.postid }}</span>
      <p v-if="this.operateType == 'issues'">
        <b-badge v-if="isOpen" variant="success" disabled size="sm">Opened</b-badge>
        <b-badge v-else variant="danger" disabled size="sm">Closed</b-badge>
        &nbsp;
        {{ poster }} opened this issue {{ date }} · {{ commetsNumber }} comments
      </p>
      <p v-else-if="this.operateType=='topic'">
        <b-badge v-if="isOpen" variant="success" disabled size="sm">Opened</b-badge>
        <b-badge v-else variant="danger" disabled size="sm">Closed</b-badge>
        &nbsp;
        {{ poster }} opened this topic {{ date }} · {{ commetsNumber }} comments
      </p>
      <p v-else-if="isOpen">
        <b-badge variant="success">Open</b-badge>
        {{ pullUser }} wants to merge {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}
      </p>
      <p v-else-if="status =='Closed'">
        <b-badge variant="danger">Closed</b-badge>
      </p>
      <p v-else>
        <b-badge variant="info">Merged</b-badge>
        {{ pullUser }} merged asdfaadsfa {{ commitsNumber }} commits into {{ pullTo }} from {{ pullFrom }}
      </p>
    </div>

    <b-nav v-if="this.operateType == 'pull'" tabs>
      <b-nav-item :active="$route.name=='PullConversion'" :to="fullPullName()">Conversion</b-nav-item>
      <b-nav-item :active="$route.name=='PullCommits'" :to="fullPullName()+'/commits'">Commits</b-nav-item>
    </b-nav>

    <b-card
      no-body
      v-for="reply in replys"
      :key="reply.comment_id"
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

    <b-card v-if="replys==''">no replys</b-card>

    <b-card style="width: 60%">
      <b-form>
        <b-form-textarea
          v-model="content"
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
  props: {
    operateType: {
      // type: String
      validator: function(value) {
        return ["topic", "issues", "pull"].indexOf(value) !== -1;
      }
    }
  },
  data() {
    return {
      title: "",
      poster: "",
      date: "",
      commetsNumber: "",
      replys: [],
      content: "",
      show: true,
      status: "Open",
      commitsNumber: "",
      pullTo: "",
      pullFrom: ""
    };
  },
  created() {
    if (this.operateType == "topic" || this.operateType == "issues") {
      this.getIssuesData();
    } else {
      this.getPullData();
    }
  },
  watch: {
    $route: "getData"
  },
  methods: {
    fullUrl() {
      if (this.operateType == "issues") {
        return this.fullIssueName();
      } else if (this.operateType == "pull") {
        return this.fullPullName();
      } else {
        return this.fullTopicName();
      }
    },
    fullTopicName() {
      let param = this.$route.params;
      return "/topics/" + param.postid;
    },
    fullPullName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/pull/" + param.postid;
    },
    fullIssueName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/issues/" + param.postid;
    },
    closeIssue() {
      axios({
        method: "POST",
        url: this.fullUrl(),
        data: {
          action: "closeIssue",
          content: this.content
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.status = "Closed";
          console.log("this issue is closed");
        } else {
          console.log(response.data.error);
        }
      });
    },
    reopenIssue() {
      axios({
        method: "POST",
        url: this.fullUrl(),
        data: {
          action: "reopenIssue",
          content: this.content
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.status = "Open";
          console.log("this issue is opend");
        } else {
          console.log(response.data.error);
        }
      });
    },
    comment() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullUrl()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   commenter: "C"
      // });
      axios({
        method: "POST",
        url: this.fullUrl(),
        data: {
          action: "newComment",
          content: this.content
        }
      }).then(response => {
        if (response.data.state == "ok") {
          let tmp = {};
          tmp["commenter"] = response.data.poster;
          tmp["address_time"] = "just now";
          tmp["content"] = this.content;
          this.replys.push(tmp);
          this.content = "";
        } else {
          console.log(response.data.error);
        }
      });
    },
    getPullData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullUrl()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   title: "a topic",
      //   status: "Merged",
      //   pullUser: "Alice",
      //   commitsNumber: 2,
      //   pullTo: "Alice:master",
      //   pullFrom: "Bob:abc",
      //   comments: [
      //     {
      //       comment_id: 0,
      //       commenter: "Alice",
      //       address_time: "1 day ago",
      //       content: "a reply text"
      //     },
      //     {
      //       comment_id: 1,
      //       commenter: "Bob",
      //       address_time: "2 days ago",
      //       content: "another reply text"
      //     }
      //   ]
      // });
      axios({
        method: "GET",
        url: this.fullUrl(),
        params: {
          ajax: 1
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.title = response.data.title;
          this.status = response.data.status;
          this.pullUser = response.data.pullUser;
          this.commitsNumber = response.data.commitsNumber;
          this.pullTo = response.data.pullTo;
          this.pullFrom = response.data.pullFrom;
          this.replys = response.data.comments;
        } else {
          console.log(response.data.error);
        }
      });
    },
    getIssuesData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullUrl()).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   title: "a title",
      //   poster: "Alice",
      //   comments: [
      //     {
      //       comment_id: 0,
      //       commenter: "Alice",
      //       address_time: "1 day ago",
      //       content: "a reply text"
      //     },
      //     {
      //       comment_id: 1,
      //       commenter: "Bob",
      //       address_time: "2 days ago",
      //       content: "another reply text"
      //     }
      //   ],
      //   show: true,
      //   status: "Open"
      // });
      axios({
        method: "GET",
        url: this.fullUrl(),
        params: {
          ajax: 1
        }
      }).then(response => {
        if (response.data.state == "ok") {
          console.log("1", response.data);
          this.title = response.data.title;
          this.poster = response.data.poster;
          this.date = response.data.comments[0].address_time;
          this.commetsNumber = response.data.comments.length;
          this.show = response.data.show;
          this.status = response.data.status;
          this.replys = response.data.comments;
          if (this.operateType == "topic") {
            document.title = this.title;
          }
        } else {
          console.log(response.data.error);
        }
      });
    }
  },
  computed: {
    isOpen() {
      return this.status == "Open";
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
