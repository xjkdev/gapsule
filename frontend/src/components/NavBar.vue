<template>
  <b-navbar toggleable="lg" type="dark" class="bg-dark">
    <b-navbar-brand href="/">Gapsule</b-navbar-brand>
    <b-navbar-toggle id="navbar-toggler" target="navbarSupportedContent">
      <span class="navbar-toggler-icon"></span>
    </b-navbar-toggle>

    <b-collapse id="navbarSupportedContent" is-nav>
      <b-navbar-nav class="mr-auto">
        <b-nav-item active href="#">
          Home
          <span class="sr-only">(current)</span>
        </b-nav-item>
        <b-nav-item href="#">Link</b-nav-item>
        <b-nav-item-dropdown text="Dropdown">
          <b-dropdown-item href="#">Action</b-dropdown-item>
          <b-dropdown-item href="#">Another action</b-dropdown-item>
          <b-dropdown-divider/>
          <b-dropdown-item href="#">Something else here</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item href="#">Disabled</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input
            size="sm"
            class="mr-sm-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <b-button variant="outline-success" class="my-2 my-sm-0" size="sm">Search</b-button>
        </b-nav-form>&nbsp;&nbsp;
        <b-nav-item to="/signin" style="color: white">Sign in</b-nav-item>&nbsp;&nbsp;
        <b-nav-form>
          <b-button to="/signup" size="sm" class="my-2 my-sm-0">Sign Up</b-button>
        </b-nav-form>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: "NavBar",
  mounted() {
    // let togglebtn = document.getElementById("navbar-toggler");
    // let collapseinit = new Collapse(togglebtn);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 90;
}
</style>
