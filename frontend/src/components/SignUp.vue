<template>
  <div id="signup">

    <h2 style="text-align: center">Join Gapsule</h2>

    <b-form @submit="onSubmit">
      <ul class="main">
        <span style="color: red">{{ errormessage }}</span>
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
            placeholder="Enter Username"
          />
        </li>

        <li class="password">
          <label for="password">Password</label>
          <span style="color: red">*</span>
          <b-input 
            v-if="hascharacter"
            v-model="password" 
            id="password" 
            required
            :state="validation" 
            type="password"
          />
          <b-input
            v-else
            v-model="password" 
            id="password" 
            required
            type="password"
          />
          <b-form-invalid-feedback v-if="hascharacter" :state="validation">
            Your password must be 6-18 characters long
          </b-form-invalid-feedback>
          <b-form-valid-feedback v-if="hascharacter" :state="validation">
            Looks good
          </b-form-valid-feedback>
        </li>

        <li class="operation">
          <b-button type="submit" variant="primary" class="submit">Next</b-button>
        </li>
      </ul>
    </b-form>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      errormessage: ''
    }
  },
  methods: {
    onSubmit() {
      axios({
        method: 'POST',
        url: '/signup',
        data: {
          ajax: 1,
          username: this.username,
          email: this.email,
          password: this.password
        },
      }).then((response) =>{
        if(response.data.state == 'ok') {
          this.$router.replace('/signup/verify');
        }else {
          this.errormessage = response.data.error;
        }
      }).catch((error) =>{
        console.log(error);
      })
    }
  },
  computed: {
    validation() {
      return this.password.length >= 6 && this.password.length <= 18
    },
    hascharacter() {
      return this.password.length > 0
    }
  }
};
</script>

<style scoped>
#signup {
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
</style>
