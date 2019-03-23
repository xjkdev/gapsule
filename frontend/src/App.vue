<template>
  <b-container id="app" fluid>
    <b-row>
      <b-col md="3" lg="2" id="sidebar" class="d-none d-md-block bg-light">
        <SideBar/>
      </b-col>
      <b-col md="9" lg="10">
        <router-view style="margin-top: 1%;"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import SideBar from "@/components/SideBar.vue";

export default {
  name: "App",
  components: { SideBar }
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
