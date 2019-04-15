import Vue from 'vue'
import Router from 'vue-router'
import DashBoard from '@/components/DashBoard'
import Repo from '@/components/Repo'
import Topic from "@/components/Topic"
import SignIn from "@/components/SignIn"
import SignUp from "@/components/SignUp"
import SignUpVerify from "@/components/SignupVerify"
import SignupFinishing from "@/components/SignupFinishing"
import IssuesPulls from "@/components/IssuesPulls"
import NewIssue from "@/components/NewIssue"
import PullCompare from "@/components/PullCompare"
import PullConversion from "@/components/PullConversion"
import PullCommits from "@/components/PullCommits"
import FileContent from "@/components/FileContent"
import NewRepo from "@/components/NewRepo"

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/new', name: 'NewRepo', component: NewRepo, meta: { title: 'Create a New Repository' } },
    { path: '/signin', name: 'SignIn', component: SignIn, meta: { title: 'SignIn' } },
    { path: '/signup', name: 'SignUp', component: SignUp, meta: { title: 'Join Gapsule' } },
    {
      path: '/signup/verify',
      name: 'SignupVerify',
      component: SignUpVerify,
      meta: { title: 'Signup Verify' }
    },
    {
      path: '/signup/finishing',
      name: 'SignupFinishing',
      component: SignupFinishing,
      meta: { title: 'Signup Finishing' }
    },
    { path: '/', name: 'DashBoard', component: DashBoard },
    {
      path: '/topics/:title',
      name: 'Topic',
      component: Topic,
      meta() { return this.params.title }
    },
    {
      path: '/:owner/:repo/issues',
      name: 'Issues',
      component: IssuesPulls,
      props: {
        isIssuePage: true,
        operateType: 'issues',
      },
      meta() { return 'Issues ' + this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/issues/new',
      name: 'Issues',
      component: NewIssue,
      meta() { return 'New Issues · ' + this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/issues/:issueid',
      name: 'Issues',
      component: Topic,
      meta() { return 'Issues ' + this.params.owner + '/' + this.params.repo + '/' + this.params.issueid }
    },
    {
      path: '/:owner/:repo/pull',
      name: 'PullRequest',
      component: IssuesPulls,
      props: {
        isIssuePage: false,
        operateType: 'pull',
      },
      meta() { return 'PullRequest · ' + this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/compare',
      name: 'PullCompare',
      component: PullCompare,
      meta() { return 'Compare · ' + this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/pull/:pullid',
      name: 'PullConversion',
      component: PullConversion,
      meta() { return 'PullRequest · ' + this.params.owner + '/' + this.params.repo + '/' + this.params.pullid }
    },
    {
      path: '/:owner/:repo/pull/:pullid/commits',
      name: 'PullCommits',
      component: PullCommits,
      meta() { return 'PullRequest · ' + this.params.owner + '/' + this.params.repo + '/' + this.params.pullid + '/commits' }
    },
    {
      path: '/:owner/:repo/blob/(.*)',
      name: 'FileContent',
      component: FileContent,
      meta() { return this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo(.*)',
      name: 'Repo',
      component: Repo,
      meta() { return this.params.owner + '/' + this.params.repo }
    }]
})
