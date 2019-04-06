import Vue from 'vue'
import Router from 'vue-router'
import DashBoard from '@/components/DashBoard'
import Repo from '@/components/Repo'
import Topic from "@/components/Topic"
import SignIn from "@/components/SignIn"
import SignUp from "@/components/SignUp"
import SignUpVerify from "@/components/SignupVerify"
import SignupFinishing from "@/components/SignupFinishing"
import Issues from "@/components/Issues"
import NewIssue from "@/components/NewIssue"

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/signin', name: 'SignIn', component: SignIn, meta: {title: 'SignIn'} },
    { path: '/signup', name: 'SignUp', component: SignUp, meta: {title: 'Join Gapsule'} },
    { path: '/signup/verify',
      name: 'SignupVerify', 
      component: SignUpVerify ,
      meta: { title: 'Signup Verify' }
    },
    { path: '/signup/finishing', 
      name: 'SignupFinishing', 
      component: SignupFinishing,
      meta: { title: 'Signup Finishing' }
    },
    { path: '/', name: 'DashBoard', component: DashBoard },
    { path: '/:owner/:repo', 
      name: 'Repo', 
      component: Repo, 
      meta() { return this.params.owner+'/'+this.params.repo } 
    },
    { path: '/topics/:title',
      name: 'Topic', 
      component: Topic,

    },
    { path: '/:owner/:repo/issues',
      name: 'Issues', 
      component: Issues,
      meta() { return 'Issues '+this.params.owner+'/'+this.params.repo }
    },
    { path: '/:owner/:repo/issues/new', 
      name: 'NewIssue', 
      component: NewIssue,
      meta() { return 'New Issues '+this.params.owner+'/'+this.params.repo }
    },
    { path: '/:owner/:repo/issues/:issueid', name: 'Issue', component: Topic },
    {
      path: '/:owner/:repo/pull/:issueid',
      name: 'PullRequest',
      component: Topic
    }]
})
