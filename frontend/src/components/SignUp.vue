<template>
  <div id="signup">

    <h2 style="text-align: center">Join Gapsule</h2>

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

        <li class="email">
          <label for="email">Email</label>
          <b-form-input
            id="email"
            type="email"
            v-model="form.email"
            required
            placeholder="Enter Username"
          />
        </li>

        <li class="password">
          <label for="password">Password</label>
          <b-input 
            v-model="form.password" 
            id="password" 
            required
            :state="validation" 
            type="password"
          />
          <b-form-invalid-feedback :state="validation">
            Your password must be 6-18 characters long
          </b-form-invalid-feedback>
          <b-form-valid-feedback :state="validation">
            Looks good
          </b-form-valid-feedback>
        </li>

        <li class="operation">
          <b-button type="submit" variant="primary" class="submit">Submit</b-button>
          <b-button type="reset" variant="danger" class="reset">Reset</b-button>
        </li>
      </ul>
    </b-form>

  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
        email: ''
      },
      show: true
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
    },
    onReset(event) {
      event.preventDefault();
      this.form.username = '';
      this.form.password = '';
      this.form.email = '';
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      })
    }
  },
  computed: {
    validation() {
      return this.form.password.length >= 6 && this.form.password.length <= 18
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
.reset {
  margin-left: 5px;
}
</style>
