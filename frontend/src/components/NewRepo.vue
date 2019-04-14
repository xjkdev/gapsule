<template>
  <div style="width: 60%; margin: 0 auto; margin-bottom: 30px;">
    <div class="head">
      <h2>Create a new repository</h2>
      <p style="color: #586069">
        A repository contains all project files,
        including the revision history. Already have a project repository elsewhere?
      </p>
      <router-link to="/new/import">Import a repository</router-link>
    </div>

    <b-row>
      <b-col cols="3">
        <strong>Owner</strong>
        <b-form-select size="md" v-model="creator" :options="options"></b-form-select>
      </b-col>
      <b-col cols="4" offset="1">
        <span>
          <strong>Repository name</strong>
        </span>&nbsp;
        <span style="color: red">*</span>
        <b-form-input v-model="reponame" placeholder="enter your repository name"></b-form-input>
      </b-col>
    </b-row>

    <p>Great repository names are short and memorable</p>

    <label for="description">
      <strong>Description</strong>
      (optional)
    </label>
    <b-form-input id="description" type="text" v-model="description"></b-form-input>

    <hr style="margin-top: 30px">

    <b-form-group>
      <b-form-radio v-model="repoPropertySelect" name="public-radios" value="Public">
        <h6>Public</h6>
        <p>Anyone can see this repository. You choose who can commit.</p>
      </b-form-radio>
      <b-form-radio v-model="repoPropertySelect" name="private-radios" value="Private">
        <h6>Private</h6>
        <p>You choose who can see and commit to this repository.</p>
      </b-form-radio>
    </b-form-group>

    <hr>

    <b-button variant="success" type="submit" @click.prevent="submit">Create Repository</b-button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      creator: "",
      reponame: "",
      description: "",
      options: [],
      repoPropertySelect: ""
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    getData() {
      axios({
        method: "GET",
        url: "/new",
        params: { ajax: 1 }
      }).then(response => {
        if (response.data.state == "ok") {
          this.options = response.data.options;
          this.creator = this.options[0];
        } else {
          console.log(response.data.error);
        }
      });
    },
    submit() {
      axios({
        method: "POST",
        url: "/new",
        data: {
          creator: this.creator,
          reponame: this.reponame,
          description: this.description,
          repoVisibility: this.repoPropertySelect == "Public"
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.$router.push("/" + this.creator + "/" + this.reponame);
        } else {
          console.log(response.data.error);
        }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard > :not(first-child) {
  margin-top: 1%;
}
.head {
  width: 100%;
  /* margin-top: 40px; */
  padding-bottom: 20px;
  margin-bottom: 30px;
  border-bottom: 1px solid #e1e4e8;
}
</style>
