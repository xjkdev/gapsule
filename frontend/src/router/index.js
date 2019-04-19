import Vue from 'vue'
import Router from 'vue-router'
import DashBoard from '@/components/DashBoard'
import Repo from '@/components/Repo'
import Topic from "@/components/Topic"
import SignIn from "@/components/SignIn"
import SignUp from "@/components/SignUp"
import SignUpVerify from "@/components/SignupVerify"
import SignupFinishing from "@/components/SignupFinishing"
import IssuesPullsList from "@/components/IssuesPullsList"
import NewIssue from "@/components/NewIssue"
import PullCompare from "@/components/PullCompare"
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
      path: '/topics/:postid(\\d+)',
      name: 'Topic',
      component: Topic,
      props: {
        operateType: 'topic',
      },
      meta: { title: 'topic' }
    },
    {
      path: '/:owner/:repo/issues',
      name: 'IssuesList',
      component: IssuesPullsList,
      props: {
        operateType: 'issues',
      },
      meta() { return 'Issues ' + this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/issues/new',
      name: 'NewIssue',
      component: NewIssue,
      meta() { return 'New Issues · ' + this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/issues/:postid(\\d+)',
      name: 'Issues',
      component: Topic,
      props: {
        operateType: 'issues',
      },
      meta() { return 'Issues ' + this.params.owner + '/' + this.params.repo + '/' + this.params.postid }
    },
    {
      path: '/:owner/:repo/pulls',
      name: 'PullRequestList',
      component: IssuesPullsList,
      props: {
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
      path: '/:owner/:repo/pull/:postid(\\d+)',
      name: 'PullConversion',
      component: Topic,
      props: {
        operateType: 'pull',
      },
      meta() { return 'PullRequest · ' + this.params.owner + '/' + this.params.repo + '/' + this.params.postid }
    },
    {
      path: '/:owner/:repo/pull/:pullid(\\d+)/commits',
      name: 'PullCommits',
      component: PullCommits,
      meta() { return 'PullRequest · ' + this.params.owner + '/' + this.params.repo + '/' + this.params.pullid + '/commits' }
    },
    {
      path: '/:owner/:repo/blob/:branch/:path(.*)',
      name: 'FileContent',
      component: FileContent,
      meta() { return this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo',
      name: 'Repo',
      component: Repo,
      meta() { return this.params.owner + '/' + this.params.repo }
    },
    {
      path: '/:owner/:repo/tree/:branch/:path(.*)',
      name: 'RepoTree',
      component: Repo,
      meta() { return this.params.owner + '/' + this.params.repo + ' ' + this.params.path }
    }
  ]
})
