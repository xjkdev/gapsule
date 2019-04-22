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
      <b-card-body v-if="filetext!=''">
        <table>
          <tr
            v-for="line in lines()"
            :key="line[0]"
            v-bind:class="{'active-line': $route.hash == '#L'+line[0]}"
          >
            <td class="linenumber bg-light">
              <a :href="'#L'+line[0]" :id="'#L'+line[0]">
                <pre>{{line[0]}}</pre>
              </a>
            </td>
            <td class="code">
              <pre>{{line[1]}}</pre>
            </td>
          </tr>
        </table>
      </b-card-body>
      <b-card-body v-else>
        <h5>No code in this file.</h5>
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
      filetext: "",
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
    lines() {
      if (this.filetext == "") return [];
      let result = this.filetext.split("\n");
      for (let i in result) {
        result[i] = [1 + parseInt(i), result[i]];
      }
      if (this.filetext[this.filetext.length - 1] == "\n") {
        result.pop();
      }
      return result;
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.$route.path).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   content: "fileContent"
      // });
      axios({
        method: "GET",
        url: this.$route.path,
        params: {
          ajax: 1
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.filetext = response.data.content;
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
.linenumber {
  padding: 0 0.2rem 0 0;
  width: 3rem;
}
.linenumber a {
  text-align: right;
  user-select: none;
  -moz-user-select: none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  -o-user-select: none;
}
.linenumber pre {
  text-align: right;
  margin: 0;
}
.code {
  padding: 0;
  width: 100%;
}
.active-line {
  background-color: lightblue;
}
.code pre {
  margin: 0;
}
</style>
