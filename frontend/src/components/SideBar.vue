<template>
  <div class="sidebar">
    <b-card no-body>
      <b-card-header class="bg-transparent">Projects</b-card-header>
      <b-list-group flush>
        <b-list-group-item v-for="project in projects" :key="project.repo" class="list-group-item">
          <span v-if="project.pinned" class="oi oi-pin" title="pin" aria-hidden="true"></span>
          <a :href="'/' +project.owner">{{project.owner}}</a>
          <span>/</span>
          <a :href="'/' + project.repo">{{project.repo.replace(project.owner+'/','')}}</a>
        </b-list-group-item>
      </b-list-group>
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
          <a :href="(topic.repo?'/'+topic.repo:'')+'/'+topic.type+'/'+topic.id">
            <span class="topic-prefix-brief">{{ topicPrefixBrief(topic) }}</span>
            <span class="topic-prefix">{{ topicPrefix(topic) }}</span>
            <span>{{topic.title}}</span>
          </a>
        </b-list-group-item>
      </b-list-group>
    </b-card>
    <b-card no-body>
      <b-card-header>People</b-card-header>
      <b-list-group flush>
        <b-list-group-item v-for="person in people" :key="person.name">
          <span v-if="person.pinned" class="oi oi-pin" title="pin" aria-hidden="true"></span>
          <a :href="'/' +person.name">{{person.name}}</a>
        </b-list-group-item>
      </b-list-group>
    </b-card>
  </div>
</template>
<script>
function repoName(s) {
  let r = s.match(/[^/]+\/(.*)/);
  return r ? r[1] : "";
}
export default {
  name: "SideBar",
  data() {
    return {
      projects: [
        {
          owner: "Cooperation",
          repo: "Cooperation/A"
        },
        { owner: "Alice", repo: "Alice/B" },
        { owner: "Bob", repo: "Bob/C" }
      ],
      topics: [
        {
          type: "issues",
          id: 11,
          repo: "Cooperation/A",
          title: "something broken.",
          pinned: true
        },
        {
          type: "topics",
          id: 9,
          title: "Some open topics",
          repo: ""
        },
        {
          type: "pull",
          id: 343,
          title: "Fix #87",
          repo: "Bob/C"
        }
      ],
      people: [{ name: "Alice" }, { name: "Bob" }]
    };
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
