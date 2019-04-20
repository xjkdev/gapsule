<template>
  <div class="dashboard">
    <b-card v-if="notifications.length == 0">
      <b-card-text>No Notifications</b-card-text>
    </b-card>
    <b-card v-for="noti of notifications" :key="noti.notification_id" :title="noti.content">
      <b-card-text>{{'@' + noti.user + ' on ' + fromNowTime(noti.created_time)}}</b-card-text>
      <router-link
        :to="getlink(noti.content)"
        v-if="getlink(noti.content) != null"
        class="card-link"
      >read more</router-link>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
export default {
  name: "DashBoard",
  data() {
    return {
      notifications: []
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    fromNowTime(time) {
      return moment(time).fromNow();
    },
    getlink(content) {
      let m = content.match(/(\w+\/\w+)#(\d+)/);
      if (m == null) {
        m = content.match(/topic#(\d+)/);
        if (m == null) return null;
        else {
          return "/topics/" + m[2];
        }
      }
      if (content.indexOf("pull request") != -1) {
        return "/" + m[1] + "/pull/" + m[2];
      } else {
        return "/" + m[1] + "/issues/" + m[2];
      }
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet("/sidebar?ajax=1").reply(200, {
      //   state: "ok",
      //   error: "error",
      //
      // });
      axios({
        method: "GET",
        url: "/notification",
        params: {
          ajax: 1
        }
      })
        .then(response => {
          if (response.data.state == "ok") {
            this.notifications = response.data.notifications;
          } else {
            this.error = response.data.error;
            this.hasError = true;
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard > :not(first-child) {
  margin-top: 1%;
}
</style>
