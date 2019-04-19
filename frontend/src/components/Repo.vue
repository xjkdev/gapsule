<template>
  <div class="dashboard">
    <RepoNav/>

    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <div v-if="isRepoRoot" style="padding: 0.2rem 1rem 0.2rem 1rem">descriptions</div>

    <b-nav v-if="isRepoRoot" pills fill class="border rounded" style=" padding: 0.2rem 0">
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

    <div style="white-space: nowrap; overflow-x: hidden;">
      <div style="display: inline-block">
        <b-dropdown variant="info" boundary="window" size="sm" :text="'Branch: ' + currentBranch">
          <b-dropdown-item
            v-for="branch in branches"
            :key="branch"
            @click="currentBranch=branch"
          >{{ branch }}</b-dropdown-item>
        </b-dropdown>
      </div>
      <button
        type="button"
        class="d-none d-md-inline-block btn btn-sm btn-secondary"
        @click.prevent="newPull"
        style="display: inline-block; margin-left: 5px;"
      >New pull request</button>
      <div class="clone" style="float: right">
        <b-dropdown variant="success" boundary="window" size="sm" text="Clone or download">
          <b-dropdown-item
            @click.prevent="clone"
          >Clone: http://gapsule.com/{{$route.params.owner}}/{{$route.params.repo}}.git</b-dropdown-item>
          <b-dropdown-item @click.prevent="download">Download Zip</b-dropdown-item>
        </b-dropdown>
      </div>
      <b-btn-group class="-md-inline-flex file-button" style="float: right; margin-right: 5px;">
        <b-button variant="secondary" size="sm">Create new file</b-button>
        <b-button variant="secondary" size="sm">Upload files</b-button>
        <b-button variant="secondary" size="sm">Find file</b-button>
      </b-btn-group>&nbsp;
    </div>

    <b-card no-body class="filelist">
      <b-card-header>file list</b-card-header>
      <b-list-group flush>
        <b-list-group-item v-if="allFiles.length==0">
          <p>no file</p>
        </b-list-group-item>
        <b-list-group-item v-for="folderData in folders" :key="folderData">
          <img src="../images/folder.png">
          <router-link
            v-if="isRepoRoot"
            :to="repoName()+'/tree/'+currentBranch+'/'+folderData"
            @click.native="handleFileList()"
          >{{ folderData }}</router-link>
          <router-link
            v-else
            :to="$route.path+'/'+folderData"
            @click.native="handleFileList()"
          >{{ folderData }}</router-link>
        </b-list-group-item>
        <b-list-group-item v-for="fileData in files" :key="fileData">
          <img src="../images/file.png">
          <router-link :to="nextURL(fileData)">{{ fileData }}</router-link>
        </b-list-group-item>
      </b-list-group>
    </b-card>

    <b-card no-body>
      <b-card-header>readme</b-card-header>
      <b-card-body v-if="readme">{{ readme }}</b-card-body>
      <b-card-body v-else>no readme text</b-card-body>
    </b-card>
  </div>
</template>

<script>
import RepoNav from "@/components/RepoNav.vue";
import axios from "axios";
// import MockAdapter from "axios-mock-adapter";
export default {
  name: "Profile",
  data() {
    return {
      commitNumber: "",
      branchNumber: "",
      releaseNumber: "",
      contributorNumber: "",
      currentBranch: "master",
      branches: {},
      folders: [],
      files: [],
      allFiles: [],
      readme: "",
      error: "",
      hasError: false
    };
  },
  created() {
    this.getData();
  },
  mounted() {
    if (window.history && window.history.pushState) {
      history.pushState(null, null, document.URL);
      window.addEventListener("popstate", this.handleFileList, false);
    }
  },
  destroyed() {
    window.removeEventListener("popstate", this.goBack, false);
  },
  methods: {
    repoName() {
      let tmp = this.$route.path.split("/");
      return tmp[0] + "/" + tmp[1] + "/" + tmp[2];
    },
    newPull() {
      this.$router.push(this.repoName() + "/compare");
    },
    nextURL(fileData) {
      if (this.$route.path.indexOf("tree") == -1) {
        return this.repoName() + "/blob/" + this.currentBranch + "/" + fileData;
      } else {
        return this.$route.path.replace("tree", "blob") + "/" + fileData;
      }
    },
    handleFileList() {
      let tmpFileList = [];
      let i;
      if (this.isRepoRoot) {
        let currentFileLocation = this.$route.path.replace(
          this.repoName() + "/tree/" + this.currentBranch + "/",
          ""
        );
        for (i = 0; i < this.allFiles.length; i++) {
          if (this.allFiles[i].indexOf(currentFileLocation + "/") == 0) {
            let tmpStr = this.allFiles[i].replace(
              currentFileLocation + "/",
              ""
            );
            tmpFileList.push(tmpStr);
          }
        }
      } else {
        tmpFileList = this.allFiles;
      }
      this.changeFileList(tmpFileList);
    },
    changeFileList(files) {
      this.folders = [];
      this.files = [];
      console.log(files);
      for (let file of files) {
        let name = file[0];
        if (
          name.indexOf("/") != -1 &&
          this.folders.indexOf(name.split("/")[0]) == -1
        ) {
          this.folders.push(name.split("/")[0]);
        } else if (name.indexOf("/") == -1) {
          this.files.push(name);
        }
      }
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet(this.$route.path).reply(200, {
      //   state: "ok",
      //   error: "error",
      //   commitNumber: 1,
      //   branchNumber: 2,
      //   releaseNumber: 3,
      //   contributorNumber: 4,
      //   readme: "readme",
      //   files: [
      //     // ["folder1/folder2/folder3/a.py", ""],
      //     // ["folder4/folder5/b.vue", ""],
      //     // ["folder1/folder2/xx", ""],
      //     // ["folder1/c.txt", ""],
      //     ["d.js", ""]
      //   ],
      //   branches: ["master", "develop"]
      // });
      axios({
        method: "GET",
        url: this.$route.path,
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
          this.branches = response.data.branches;
          this.allFiles = response.data.allFiles;
          this.changeFileList(this.allFiles);
        } else {
          this.error = response.data.error;
          this.hasError = true;
        }
      });
    }
  },
  computed: {
    isRepoRoot() {
      return this.$route.params.path == undefined;
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
@media (max-width: 1000px) {
  .file-button {
    display: none;
  }
}
</style>
