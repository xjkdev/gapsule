<template>
  <div>
    <el-steps :active="1" finish-status="success" align-center style="margin: 0 auto">
      <el-step title="Sign Up"></el-step>
      <el-step title="Verify Your Password"></el-step>
      <el-step title="Fill In Your Information"></el-step>
    </el-steps>
    <div id="login">
      <h3 style="text-align: center">Verify your password</h3>

      <b-form @submit.prevent="onSubmit">
        <ul class="main">
          <li class="username">
            <label for="username">Username</label>
            <b-form-input id="username" type="text" readonly v-model="username"/>
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
      password: "",
      token: ""
    };
  },
  created() {
    this.username = this.$route.query.username;
    this.token = this.$route.query.token;
    if (this.username == undefined || this.token == undefined) {
      window.location.replace("/");
    }
  },
  methods: {
    onSubmit() {
      axios({
        method: "POST",
        url: "/signup/verify",
        data: {
          username: this.username,
          password: this.password,
          token: this.token
        }
      }).then(response => {
        if (response.data.state == "ok") {
          globals.cache.password = this.password;
          globals.cache.username = this.username;
          globals.cache.token = this.token;
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
  margin-top: 10px;
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
