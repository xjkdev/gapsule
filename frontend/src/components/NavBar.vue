<template>
  <b-navbar toggleable="lg" type="dark" class="bg-dark">
    <b-navbar-brand to="/">Gapsule</b-navbar-brand>
    <b-navbar-toggle id="navbar-toggler" target="navbarSupportedContent">
      <span class="navbar-toggler-icon"></span>
    </b-navbar-toggle>

    <b-collapse id="navbarSupportedContent" is-nav>
      <b-navbar-nav class="mr-auto">
        <b-nav-item to="#">
          Pull requests
          <span class="sr-only">(current)</span>
        </b-nav-item>
        <b-nav-item to="#">Issues</b-nav-item>
        <b-nav-item to="#">Marketplace</b-nav-item>
        <!-- <b-nav-item-dropdown text="Dropdown">
          <b-dropdown-item to="#">Action</b-dropdown-item>
          <b-dropdown-item to="#">Another action</b-dropdown-item>
          <b-dropdown-divider/>
          <b-dropdown-item to="#">Something else here</b-dropdown-item>
        </b-nav-item-dropdown>-->
        <b-nav-item to="#">Explore</b-nav-item>
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
        <b-nav-item href="/signin" style="color: white" v-if="!username">Sign in</b-nav-item>&nbsp;&nbsp;
        <b-nav-form>
          <b-button href="/signup" size="sm" class="my-2 my-sm-0" v-if="!username">Sign Up</b-button>
        </b-nav-form>

        <img v-if="icon" :src="icon" alt="UserIcon">
        <b-dropdown v-if="username" :text="username" right size="sm">
          <b-dropdown-item>
            Signed in as
            <strong>{{ username }}</strong>
          </b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item>Your profile</b-dropdown-item>
          <b-dropdown-item>Your repositories</b-dropdown-item>
          <b-dropdown-item>Your projects</b-dropdown-item>
          <b-dropdown-item>Your stars</b-dropdown-item>
          <b-dropdown-item>Your gists</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item>Help</b-dropdown-item>
          <b-dropdown-item>Settings</b-dropdown-item>
          <b-dropdown-item>Sign out</b-dropdown-item>
        </b-dropdown>
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
  },
  created() {
    this.username = this.getCookie("username");
    this.icon = this.getCookie("icon");
  },
  watch: {
    $route: "getData"
  },
  data() {
    return {
      username: "",
      icon: ""
    };
  },
  methods: {
    getCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(";");
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
          c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
          return c.substring(nameEQ.length, c.length);
        }
      }
      return "";
    }
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
