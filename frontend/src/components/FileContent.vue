<template>
  <div class="dashboard">
    <RepoNav/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <b-card no-body header="filename" header-tag="header">
      <span slot="header">{{ fileName() }}</span>
      <b-card-body>
        <p class="card-text">{{ filetext }}</p>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import RepoNav from "@/components/RepoNav.vue";
import axios from "axios";
// import MockAdapter from "axios-mock-adapter";
export default {
  data() {
    return {
      filetext: "no code in this file",
      error: "",
      hasError: false
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    fileName() {
      let tmp = this.$route.path.split("/");
      let len = tmp.length;
      return tmp[len - 1];
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.$route.path).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   filetext: "fileContent"
      // });
      axios({
        method: "GET",
        url: this.$route.path,
        params: {
          ajax: 1
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.filetext = response.data.filetext
            ? response.data.filetext
            : "no code in this file";
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
