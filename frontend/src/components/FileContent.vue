<template>
  <div class="dashboard">
    <RepoNav/>

    <b-card no-body header="fileName" header-tag="fileName">
      <span slot="fileName">{{ fileName() }}</span>
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
      filetext: ""
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
          this.filetext = response.data.filetext;
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
