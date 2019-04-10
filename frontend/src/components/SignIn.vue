<template>
  <div id="login">
    <div class="logo">
      <img src="../images/logo.jpg" alt="Logo">
    </div>

    <h2 style="text-align: center">Sign in to Gapsule</h2>

    <b-form @submit="onSubmit">
      <ul class="main">
        <li class="username">
          <label for="username">Username</label>
          <b-form-input
            id="username"
            type="text"
            v-model="username"
            required
            placeholder="Enter Username"
          />
        </li>

        <li class="password">
          <label for="password">Password</label>
          <a href="#" style="float: right">Forget Password?</a>
          <b-form-input
            id="password"
            type="password"
            v-model="password"
            required
            placeholder="Enter password"
          />
        </li>

        <li class="operation">
          <b-button block type="submit" variant="primary" class="submit">Submit</b-button>
        </li>
      </ul>
    </b-form>

    <div class="create-account">
      <span>New to Gapsule?</span>
      <router-link to="/signup">Create an account</router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignIn",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    onSubmit() {
      axios({
        method: "POST",
        url: "/signin",
        data: {
          ajax: 1,
          username: this.username,
          password: this.password
        }
      }).then(response => {
        if (response.status == 200) {
          this.$router.replace("/index");
        }
      });
    }
  }
};
</script>

<style scoped>
#login {
  width: 320px;
  height: 100%;
  margin: 0 auto;
}
.logo {
  width: 100%;
  height: 16%;
  position: relative;
}
.logo img {
  width: 60px;
  height: 60px;
  background-size: 100%;
  position: absolute;
  left: 50%;
  top: 50%;
  margin-left: -30px;
  margin-top: -30px;
}
#password {
  display: inline-block;
}
ul {
  list-style: none;
  margin-top: 1rem;
  background-color: rgb(255, 255, 220);
  border: 1px solid #d7dee2;
}
ul li {
  list-style: none;
  width: 100%;
  margin-left: -20px;
  padding: 0.6rem 0;
}
.create-account {
  width: 100%;
  height: 45px;
  margin-top: 0.6rem;
  background-color: rgb(255, 255, 220);
  border: 1px solid #d7dee2;
  text-align: center;
}
.create-account * {
  line-height: 45px;
}
</style>
