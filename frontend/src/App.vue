<template>
  <b-container id="app" fluid>
    <b-row>
      <b-col v-if="showSidebar" md="3" lg="2" id="sidebar" class="d-none d-md-block bg-light">
        <SideBar ref="sidebar"/>
      </b-col>
      <b-col :md="showSidebar?9:12" :lg="showSidebar?10:12">
        <router-view style="margin-top: 1%;"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import SideBar from "@/components/SideBar.vue";
export default {
  name: "app",
  data() {
    return {
      showSidebar: true
    };
  },
  components: {
    SideBar
  },
  created() {
    this.$router.afterEach((to, _from) => {
      this.showSidebar = !to.name.match(/^Sign|NonExisting|NewRepo/);
    });
    this.showSidebar = !this.$route.name.match(/^Sign|NonExisting|NewRepo/);
  }
};
</script>

<style scoped>
#sidebar {
  height: calc(100vh - 56px);
  position: sticky;
  top: 56px;
  overflow-y: auto;
}
</style>
