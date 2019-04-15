<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <b-card style="width: 60%">
      <b-form @submit.prevent="onSubmit">
        <b-form-input v-model="title" placeholder="Title" required style="margin-bottom: 10px"></b-form-input>
        <b-form-textarea
          v-model="commet"
          placeholder="Leave a commet"
          size="md"
          rows="5"
          max-rows="10"
          style="margin-bottom: 10px"
        ></b-form-textarea>
        <b-button variant="success" type="submit" style="float: right">Submit new issue</b-button>
      </b-form>
    </b-card>
  </b-container>
</template>

<script>
import RepoNav from "@/components/RepoNav";
import axios from "axios";
// import MockAdapter from "axios-mock-adapter";
export default {
  name: "Issues",
  data() {
    return {
      title: "",
      commet: ""
    };
  },
  methods: {
    fullIssuesName() {
      let param = this.$route.params;
      return "/" + param.owner + "/" + param.repo + "/issues";
    },
    onSubmit() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.fullIssuesName() + "/new").reply(200, {
      //   state: "ok",
      //   error: "error",
      //   issueid: 1
      // });
      axios({
        method: "POST",
        url: this.fullIssuesName() + "/new",
        data: {
          owner: this.$route.params.owner,
          repo: this.$route.params.repo,
          title: this.title,
          commet: this.commet
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.$router.push(
            this.fullIssuesName() + "/" + response.data.issueid
          );
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
