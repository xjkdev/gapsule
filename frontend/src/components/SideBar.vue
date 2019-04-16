<template>
  <div class="sidebar">
    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <b-card no-body>
      <b-card-header class="bg-transparent">Projects</b-card-header>
      <b-list-group flush>
        <b-list-group-item v-for="project in projects" :key="project.repo" class="list-group-item">
          <span v-if="project.pinned" class="oi oi-pin" title="pin" aria-hidden="true"></span>
          <router-link :to="'/' +project.owner">{{project.owner}}</router-link>
          <span>/</span>
          <router-link :to="'/' + project.repo">{{project.repo.replace(project.owner+'/','')}}</router-link>
        </b-list-group-item>
      </b-list-group>
      <p v-if="projects==''">no project yet</p>
    </b-card>

    <b-card no-body>
      <b-card-header>Topics</b-card-header>
      <b-list-group flush>
        <b-list-group-item
          class="topic-item"
          v-for="topic in topics"
          :key="topic.type+'/'+topic.repo+'/'+topic.id"
        >
          <span v-if="topic.pinned" class="oi oi-pin" title="pin" aria-hidden="true"></span>
          <router-link :to="(topic.repo?'/'+topic.repo:'')+'/'+topic.type+'/'+topic.id">
            <span class="topic-prefix-brief">{{ topicPrefixBrief(topic) }}</span>
            <span class="topic-prefix">{{ topicPrefix(topic) }}</span>
            <span>{{topic.title}}</span>
          </router-link>
        </b-list-group-item>
      </b-list-group>
      <p v-if="topics==''">no topic yet</p>
    </b-card>

    <b-card no-body>
      <b-card-header>People</b-card-header>
      <b-list-group flush>
        <b-list-group-item v-for="person in people" :key="person.name">
          <span v-if="person.pinned" class="oi oi-pin" title="pin" aria-hidden="true"></span>
          <router-link :to="'/' +person.name">{{person.name}}</router-link>
        </b-list-group-item>
      </b-list-group>
      <p v-if="people==''">no people yet</p>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
// import MockAdapter from "axios-mock-adapter";
function repoName(s) {
  let r = s.match(/[^/]+\/(.*)/);
  return r ? r[1] : "";
}
export default {
  name: "SideBar",
  data() {
    return {
      projects: [],
      topics: [],
      people: [],
      error: "",
      hasError: false
    };
  },
  created() {
    this.getData();
  },
  watch: {
    $route: "getData"
  },
  methods: {
    repoName: repoName,
    topicPrefixBrief(topic) {
      if (topic.type == "topics") {
        return "";
      }
      let name = repoName(topic.repo);
      let idsign = topic.type == "pull" ? "PR" : "#";
      return "[" + name + " " + idsign + topic.id + "]";
    },
    topicPrefix(topic) {
      if (topic.type == "topics") {
        return "";
      }
      let name = topic.repo;
      let idsign = topic.type == "pull" ? "PR" : "#";
      return "[" + name + " " + idsign + topic.id + "]";
    },
    getData() {
      // let mock = new MockAdapter(axios);
      // mock.onGet("/sidebar?ajax=1").reply(200, {
      //   state: "ok",
      //   error: "error",
      //   projects: [
      //     {
      //       owner: "Cooperation",
      //       repo: "Cooperation/A"
      //     },
      //     { owner: "Alice", repo: "Alice/B" },
      //     { owner: "Bob", repo: "Bob/C" }
      //   ],
      //   topics: [
      //     {
      //       type: "issues",
      //       id: 11,
      //       repo: "Cooperation/A",
      //       title: "something broken.",
      //       pinned: true
      //     },
      //     {
      //       type: "topics",
      //       id: 9,
      //       title: "Some open topics",
      //       repo: ""
      //     },
      //     {
      //       type: "pull",
      //       id: 343,
      //       title: "Fix #87",
      //       repo: "Bob/C"
      //     }
      //   ],
      //   people: [{ name: "Alice" }, { name: "Bob" }]
      // });
      axios({
        method: "GET",
        url: "/sidebar?ajax=1",
        params: {
          ajax: 1
        }
      }).then(response => {
        if (response.data.state == "ok") {
          this.projects = response.data.projects;
          this.topics = response.data.topics;
          this.people = response.data.people;
        } else {
          this.error = response.data.error;
          this.hasError = true;
        }
      });
    }
  }
};
</script>

<style scoped>
.sidebar > .card:first-child {
  margin-top: 1rem;
}
.sidebar > .card {
  margin-bottom: 1rem;
}

.sidebar .list-group-item {
  padding: 0.3rem 0.3rem 0.3rem 0.3rem;
}

.card {
  border: none;
  background-color: transparent !important;
}

.card-header {
  padding-left: 0rem;
  background-color: transparent !important;
}

.card .list-group-item {
  background-color: transparent !important;
  border: none;
  overflow-x: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.card .list-group-item:hover {
  white-space: normal;
}

.topic-item .topic-prefix {
  display: none;
}
.topic-item:hover .topic-prefix {
  display: inline;
}
.topic-item:hover .topic-prefix-brief {
  display: none;
}

.topic-prefix,
.topic-prefix-brief {
  font-size: 0.8em;
}

span.oi.oi-pin {
  font-size: 0.8em;
}
</style>
