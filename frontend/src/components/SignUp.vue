<template>
  <div>
    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <el-steps :active="0" finish-status="success" align-center style="margin: 0 auto">
      <el-step title="Sign Up"></el-step>
      <el-step title="Verify Your Password"></el-step>
      <el-step title="Fill In Your Information"></el-step>
    </el-steps>

    <div id="signup">
      <h2 style="text-align: center">Join Gapsule</h2>

      <b-form @submit.prevent="onSubmit">
        <ul class="main">
          <span style="color: red">{{ error }}</span>
          <li class="username">
            <label for="username">Username</label>
            <span style="color: red">*</span>
            <b-form-input
              id="username"
              type="text"
              v-model="username"
              required
              placeholder="Enter Username"
            />
          </li>

          <li class="email">
            <label for="email">Email</label>
            <span style="color: red">*</span>
            <b-form-input
              id="email"
              type="email"
              v-model="email"
              required
              placeholder="Enter Email"
            />
          </li>

          <li class="password">
            <label for="password">Password</label>
            <span style="color: red">*</span>
            <b-input
              v-model="password"
              id="password"
              required
              :state="validation"
              type="password"
              placeholder="Enter Password"
            />
            <b-form-invalid-feedback :state="validation">Your password must be 6-18 characters long</b-form-invalid-feedback>
            <b-form-valid-feedback :state="validation">Looks good</b-form-valid-feedback>
          </li>

          <li class="operation">
            <b-button block type="submit" variant="primary" class="submit">Next</b-button>
          </li>
        </ul>
      </b-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignUp",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      password_entered: false,
      error: "",
      hasError: false
    };
  },
  methods: {
    onSubmit() {
      axios({
        method: "POST",
        url: "/signup",
        data: {
          username: this.username,
          email: this.email,
          password: this.password
        }
      })
        .then(response => {
          if (response.data.state == "ok") {
            if (response.data.token == null) {
              alert("the email has been sent to your mailbox");
            } else {
              this.$router.replace(
                "/signup/verify?username=" +
                  this.username +
                  "&token=" +
                  response.data.token
              );
            }
          } else {
            this.error = response.data.error;
            this.hasError = true;
          }
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  computed: {
    validation() {
      if (!this.password_entered && this.password.length == 0) return null;
      this.password_entered = true;
      return this.password.length >= 6 && this.password.length <= 18;
    }
  }
};
</script>

<style scoped>
#signup {
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
</style>
