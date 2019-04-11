<template>
  <div class="dashboard">
    <RepoNav/>

    <div style="padding: 0.2rem 1rem 0.2rem 1rem">descriptions</div>

    <b-nav pills fill class="border rounded" style=" padding: 0.2rem 0">
      <b-nav-item>
        <router-link class="nav-link" to="#">{{ commitNumber }} commits</router-link>
      </b-nav-item>
      <b-nav-item>
        <router-link class="nav-link" to="#">{{ branchNumber }} branches</router-link>
      </b-nav-item>
      <b-nav-item>
        <router-link class="nav-link" to="#">{{ releaseNumber }} releases</router-link>
      </b-nav-item>
      <b-nav-item>
        <router-link class="nav-link" to="#">{{ contributorNumber }} contributors</router-link>
      </b-nav-item>
      <b-nav-item>
        <router-link class="nav-link" to="#">View lisence</router-link>
      </b-nav-item>
    </b-nav>

    <b-row style="white-space: nowrap;overflow-x: hidden;">
      <div>
        <b-dropdown
          class="col-2"
          variant="info"
          boundary="window"
          size="sm"
          :text="'Branch: ' + currentBranch"
        >
          <b-dropdown-item v-for="branch in branches" :key="branch">{{ branch }}</b-dropdown-item>
        </b-dropdown>
      </div>
      <b-col cols="2">
        <button
          type="button"
          class="d-none d-md-inline-block btn btn-sm btn-secondary"
          @click.prevent="newPull"
        >New pull request</button>
      </b-col>
      <!-- FIXME: 改变大小时显示错误 -->
      <b-col cols="3" offset="3" style="overflow: hidden">
        <b-btn-group class="-md-inline-flex">
          <b-button variant="secondary" size="sm">Create new file</b-button>
          <b-button variant="secondary" size="sm">Upload files</b-button>
          <b-button variant="secondary" size="sm">Find file</b-button>
        </b-btn-group>&nbsp;
      </b-col>
      <div class="clone">
        <b-dropdown
          class="col-2"
          variant="success"
          boundary="window"
          right
          size="sm"
          text="Clone or download"
        >
          <b-dropdown-item
            @click.prevent="clone"
          >Clone: http://gapsule.com/{{$route.params.owner}}/{{$route.params.repo}}.git</b-dropdown-item>
          <b-dropdown-item @click.prevent="download">Download Zip</b-dropdown-item>
        </b-dropdown>
      </div>
    </b-row>

    <b-card no-body class="filelist">
      <b-card-header>file list</b-card-header>
      <b-list-group flush>
        <b-list-group-item v-for="folderData in files['folder']" :key="folderData">
          <img src="../images/folder.png">
          <router-link :to="fullRepoName()+'/tree/'+currentBranch+'/'+folderData">{{ folderData }}</router-link>
        </b-list-group-item>
        <b-list-group-item v-for="fileData in files['file']" :key="fileData">
          <img src="../images/file.png">
          <router-link :to="fullRepoName()+'/blob/'+currentBranch+'/'+fileData">{{ fileData }}</router-link>
        </b-list-group-item>
      </b-list-group>
    </b-card>

    <b-card no-body>
      <b-card-header>readme</b-card-header>
      <b-card-body>{{ readme }}</b-card-body>
    </b-card>
  </div>
</template>

<script>
import RepoNav from "@/components/RepoNav.vue";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
export default {
  name: "Profile",
  data() {
    return {
      commitNumber: "",
      branchNumber: "",
      releaseNumber: "",
      contributorNumber: "",
      currentBranch: "",
      branches: {},
      files: {},
      readme: "",
      msg: "Welcome to Your Vue.js App"
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    fullRepoName() {
      return "/" + this.$route.params.owner + "/" + this.$route.params.repo;
    },
    newPull() {
      this.$router.replace(this.fullRepoName() + "/compare");
    },
    getData() {
      let mock = new MockAdapter(axios);
      mock.onGet(this.fullRepoName()).reply(200, {
        state: "ok",
        error: "error",
        commitNumber: 1,
        branchNumber: 2,
        releaseNumber: 3,
        contributorNumber: 4,
        readme: "readme",
        files: {
          folder: ["folder1", "folder2"],
          file: ["file1", "file2"]
        },
        currentBranch: "master",
        branches: ["master"]
      });
      axios({
        method: "GET",
        url: this.fullRepoName(),
        params: {
          ajax: 1,
          owner: this.$route.params.owner,
          repo: this.$route.params.repo
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.commitNumber = response.data.commitNumber;
          this.branchNumber = response.data.branchNumber;
          this.releaseNumber = response.data.releaseNumber;
          this.contributorNumber = response.data.contributorNumber;
          this.readme = response.data.readme;
          this.files = response.data.files;
          this.currentBranch = response.data.currentBranch;
          this.branches = response.data.branches;
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
.filelist .list-group-item {
  padding: 0.3rem 1rem;
}
.card-header {
  padding: 0.3rem 1rem;
}
.clone {
  position: absolute;
  right: 0;
  z-index: 90;
}
</style>
