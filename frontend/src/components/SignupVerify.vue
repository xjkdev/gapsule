<template>
  <div id="login">
    <h3 style="text-align: center">Vertify your password</h3>

    <b-form @submit.prevent="onSubmit">
      <ul class="main">
        <li class="username">
          <label for="username">Username</label>
          <b-form-input id="username" type="text" disabled v-model="username"/>
        </li>

        <li class="password">
          <label for="password">Password</label>
          <b-form-input
            id="password"
            type="password"
            v-model="password"
            required
            placeholder="Enter password"
          />
        </li>

        <li class="operation">
          <b-button type="submit" variant="primary" class="submit">Submit</b-button>
        </li>
      </ul>
    </b-form>
  </div>
</template>

<script>
import globals from "@/globals";
import axios from "axios";
export default {
  name: "SignupVerify",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  created() {
    this.username = this.$route.query.username;
  },
  methods: {
    onSubmit() {
      axios({
        method: "POST",
        url: "/signup/verify",
        data: {
          ajax: 1,
          password: this.password
        }
      }).then(response => {
        if (response.data.state == "ok") {
          globals.cache.password = this.password;
          this.$router.replace("/signup/finishing");
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
