<template>
  <b-container class="dashboard">
    <RepoNav v-if="$route.name != 'Topic'"/>

    <h4>Compare changes</h4>
    <p>Compare changes across branches, commits, tags, and more below.</p>
  </b-container>
</template>

<script>
import RepoNav from "@/components/RepoNav";
export default {
  components: { RepoNav }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard > :not(first-child) {
  margin-top: 1%;
}
</style>
