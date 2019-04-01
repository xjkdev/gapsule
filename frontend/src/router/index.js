import Vue from 'vue'
import Router from 'vue-router'
import DashBoard from '@/components/DashBoard'
import Repo from '@/components/Repo'
import Topic from "@/components/Topic"
import SignIn from "@/components/SignIn"
import SignUp from "@/components/SignUp"
import UserInfoFilling from "@/components/UserInfoFilling"

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'DashBoard', component: DashBoard },
    { path: '/:owner/:repo', name: 'Repo', component: Repo },
    { path: '/topics/:title', name: 'Topic', component: Topic },
    { path: '/:owner/:repo/issues/:issueid', name: 'Issue', component: Topic },
    { path: '/signin', name: 'SignIn', component: SignIn },
    { path: '/signup', name: 'SignUp', component: SignUp },
    { path: '/userinfo-filling', name: 'UserInfoFilling', component: UserInfoFilling},
    {
      path: '/:owner/:repo/pull/:issueid',
      name: 'PullRequest',
      component: Topic
    }]
})
