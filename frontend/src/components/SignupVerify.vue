<template>
  <div id="login">

    <h3 style="text-align: center">Vertify your password</h3>

    <b-form @submit="onSubmit">
      <ul class="main">
        <li class="username">
          <label for="username">Username</label>
          <b-form-input
            id="username"
            type="text"
            disabled
            :placeholder="username"
          />
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
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter'
export default {
  name: 'SignupVerify',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  created() {
    this.fetchUsername()
  },
  watch: {
    '$route': 'fetchUsername'
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      let mock = new MockAdapter(axios);
      // eslint-disable-next-line
      mock.onPost('/signup/verify').reply(config => {
        // eslint-disable-next-line
        return new Promise((resolve, reject) => {
          resolve([200, {state: 'ok', error: 'error'}]);
        });
      });
      axios({
        method: 'POST',
        url: '/signup/verify',
        data: {
          ajax: 1,
          password: this.password
        }
      }).then((response) =>{
        if(response.data.state == 'ok') {
          this.$router.replace('/signup/finishing');
        }
      });
    },
    fetchUsername() {
      let mock = new MockAdapter(axios);
      // eslint-disable-next-line
      mock.onPost('/signup/verify').reply(config => {
        // eslint-disable-next-line
        return new Promise((resolve, reject) => {
          resolve([200, {state: 'ok', error: 'error', username: '123'}]);
        });
      });
      axios({
          method: 'POST',
          url: '/signup/verify',
          data: {
            ajax: 1,
          }
      }).then(response => {
          if(response.data.state == 'ok') {
              console.log(response.data.username);
              this.username = response.data.username;
          }else {
              console.log(response.data.error)
          }
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
