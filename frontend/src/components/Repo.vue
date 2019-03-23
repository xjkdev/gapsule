<template>
  <div class="dashboard">
    <RepoNav/>
    <div style="padding: 0.2rem 1rem 0.2rem 1rem">descriptions</div>
    <b-nav pills fill class="border rounded" style=" padding: 0.2rem 0">
      <b-nav-item>
        <a class="nav-link" href="#">xx commits</a>
      </b-nav-item>
      <b-nav-item>
        <a class="nav-link" href="#">xx branches</a>
      </b-nav-item>
      <b-nav-item>
        <a class="nav-link" href="#">xx releases</a>
      </b-nav-item>
      <b-nav-item>
        <a class="nav-link" href="#">xx contributors</a>
      </b-nav-item>
      <b-nav-item>
        <a class="nav-link" href="#">View lisence</a>
      </b-nav-item>
    </b-nav>
    <b-row style="white-space: nowrap;overflow-x: hidden;">
      <b-col cols="2">
        <button type="button" class="btn btn-sm btn-secondary dropdown-toggle">Branch: master</button>
      </b-col>
      <b-col cols="2">
        <button
          type="button"
          class="d-none d-md-inline-block btn btn-sm btn-secondary"
        >New pull request</button>
      </b-col>
      <!-- FIXME: 改变大小时显示错误 -->
      <b-col cols="3" offset="3">
        <b-btn-group class="d-none d-md-inline-flex">
          <b-button variant="secondary" size="sm">Create new file</b-button>
          <b-button variant="secondary" size="sm">Upload files</b-button>
          <b-button variant="secondary" size="sm">Find file</b-button>
        </b-btn-group>&nbsp;
      </b-col>
      <b-dropdown
        class="col-2"
        variant="success"
        boundary="window"
        right
        size="sm"
        text="Clone or download"
      >
        <b-dropdown-item>Clone: http...git</b-dropdown-item>
        <b-dropdown-item>Download: http...zip</b-dropdown-item>
      </b-dropdown>
    </b-row>

    <b-card no-body class="filelist">
      <b-card-header>last commit message</b-card-header>
      <b-list-group flush>
        <b-list-group-item>file1</b-list-group-item>
        <b-list-group-item>file2</b-list-group-item>
        <b-list-group-item>file3</b-list-group-item>
      </b-list-group>
    </b-card>
    <b-card no-body>
      <b-card-header>readme</b-card-header>
      <b-card-body>readme...</b-card-body>
    </b-card>
  </div>
</template>

<script>
import RepoNav from "@/components/RepoNav.vue";
export default {
  name: "Profile",
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
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
</style>
