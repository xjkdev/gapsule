<template>
  <div class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

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
        <b-button variant="success" type="submit" style="float: right">Submit new issue</b-button>
      </b-form>
    </b-card>
  </div>
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
      comment: "",
      error: "",
      hasError: false
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
          comment: this.comment
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.$router.push(
            this.fullIssuesName() + "/" + response.data.issueid
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
