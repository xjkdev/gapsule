<template>
  <div id="login">
    <div class="logo">
      <img src="../images/logo.jpg" alt="Logo">
    </div>

    <h2 style="text-align: center">Sign in to Gapsule</h2>

    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <ul class="main">
        <li class="username">
          <label for="username">Username</label>
          <b-form-input
            id="username"
            type="text"
            v-model="form.username"
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
            v-model="form.password"
            required
            placeholder="Enter password"
          />
        </li>

        <li class="operation">
          <b-button type="submit" variant="primary" class="submit">Submit</b-button>
          <b-button type="reset" variant="danger" class="reset">Reset</b-button>
        </li>
      </ul>
    </b-form>

      <div class="create-account">
        <span>New to Gapsule?</span>
        <a href="#">Create an account</a>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      show: true
    }
  },
  methods: {
    onSubmit() {
      axios({
        method: 'POST',
        data: {
          username: this.form.username,
          password: this.form.password
        }
      }).then((response) =>{
        if(response.status == 200) {
          window.location.href = '/index';
        }
      });
    },
    onReset(event) {
      event.preventDefault();
      this.form.username = '';
      this.form.password = '';
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      })
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
  border: 1px solid #D7DEE2;
}
ul li {
  list-style: none;
  width: 100%;
  margin-left: -20px;
  padding: 0.6rem 0;
}
.reset {
  margin-left: 5px;
}
.create-account {
  width: 100%;
  height: 45px;
  margin-top: 0.6rem;
  background-color: rgb(255, 255, 220);
  border: 1px solid #D7DEE2;
  text-align: center;
}
.create-account * {
  line-height: 45px;
}
</style>
