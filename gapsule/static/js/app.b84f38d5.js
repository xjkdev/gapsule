(function(t){function e(e){for(var s,n,i=e[0],l=e[1],u=e[2],p=0,m=[];p<i.length;p++)n=i[p],r[n]&&m.push(r[n][0]),r[n]=0;for(s in l)Object.prototype.hasOwnProperty.call(l,s)&&(t[s]=l[s]);c&&c(e);while(m.length)m.shift()();return o.push.apply(o,u||[]),a()}function a(){for(var t,e=0;e<o.length;e++){for(var a=o[e],s=!0,i=1;i<a.length;i++){var l=a[i];0!==r[l]&&(s=!1)}s&&(o.splice(e--,1),t=n(n.s=a[0]))}return t}var s={},r={app:0},o=[];function n(e){if(s[e])return s[e].exports;var a=s[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,n),a.l=!0,a.exports}n.m=t,n.c=s,n.d=function(t,e,a){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},n.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var s in t)n.d(a,s,function(e){return t[e]}.bind(null,s));return a},n.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],l=i.push.bind(i);i.push=e,i=i.slice();for(var u=0;u<i.length;u++)e(i[u]);var c=l;o.push([0,"chunk-vendors"]),a()})({0:function(t,e,a){t.exports=a("56d7")},"2fed":function(t,e,a){},"305d":function(t,e,a){"use strict";var s=a("2fed"),r=a.n(s);r.a},"31e0":function(t,e,a){},"329f":function(t,e,a){},"36fc":function(t,e,a){},"3a69":function(t,e,a){},"3b02":function(t,e,a){},"3b79":function(t,e,a){"use strict";var s=a("4b63"),r=a.n(s);r.a},4473:function(t,e,a){},"4b63":function(t,e,a){},5444:function(t,e,a){t.exports=a.p+"static/img/choose_icon.2185fb83.jpg"},"56d7":function(t,e,a){"use strict";a.r(e);a("cadf"),a("551c"),a("f751"),a("097d");var s=a("2b0e"),r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{attrs:{id:"app",fluid:""}},[a("b-row",[a("b-col",{staticClass:"d-none d-md-block bg-light",attrs:{md:"3",lg:"2",id:"sidebar"}},[a("SideBar")],1),a("b-col",{attrs:{md:"9",lg:"10"}},[a("router-view",{staticStyle:{"margin-top":"1%"}})],1)],1)],1)},o=[],n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"sidebar"},[a("b-card",{attrs:{"no-body":""}},[a("b-card-header",{staticClass:"bg-transparent"},[t._v("Projects")]),a("b-list-group",{attrs:{flush:""}},t._l(t.projects,function(e){return a("b-list-group-item",{key:e.repo,staticClass:"list-group-item"},[e.pinned?a("span",{staticClass:"oi oi-pin",attrs:{title:"pin","aria-hidden":"true"}}):t._e(),a("router-link",{attrs:{to:"/"+e.owner}},[t._v(t._s(e.owner))]),a("span",[t._v("/")]),a("router-link",{attrs:{to:"/"+e.repo}},[t._v(t._s(e.repo.replace(e.owner+"/","")))])],1)}),1)],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-header",[t._v("Topics")]),a("b-list-group",{attrs:{flush:""}},t._l(t.topics,function(e){return a("b-list-group-item",{key:e.type+"/"+e.repo+"/"+e.id,staticClass:"topic-item"},[e.pinned?a("span",{staticClass:"oi oi-pin",attrs:{title:"pin","aria-hidden":"true"}}):t._e(),a("router-link",{attrs:{to:(e.repo?"/"+e.repo:"")+"/"+e.type+"/"+e.id}},[a("span",{staticClass:"topic-prefix-brief"},[t._v(t._s(t.topicPrefixBrief(e)))]),a("span",{staticClass:"topic-prefix"},[t._v(t._s(t.topicPrefix(e)))]),a("span",[t._v(t._s(e.title))])])],1)}),1)],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-header",[t._v("People")]),a("b-list-group",{attrs:{flush:""}},t._l(t.people,function(e){return a("b-list-group-item",{key:e.name},[e.pinned?a("span",{staticClass:"oi oi-pin",attrs:{title:"pin","aria-hidden":"true"}}):t._e(),a("router-link",{attrs:{to:"/"+e.name}},[t._v(t._s(e.name))])],1)}),1)],1)],1)},i=[];a("4917");function l(t){var e=t.match(/[^\/]+\/(.*)/);return e?e[1]:""}var u={name:"SideBar",data:function(){return{projects:[{owner:"Cooperation",repo:"Cooperation/A"},{owner:"Alice",repo:"Alice/B"},{owner:"Bob",repo:"Bob/C"}],topics:[{type:"issues",id:11,repo:"Cooperation/A",title:"something broken.",pinned:!0},{type:"topics",id:9,title:"Some open topics",repo:""},{type:"pull",id:343,title:"Fix #87",repo:"Bob/C"}],people:[{name:"Alice"},{name:"Bob"}]}},methods:{repoName:l,topicPrefixBrief:function(t){if("topics"==t.type)return"";var e=l(t.repo),a="pull"==t.type?"PR":"#";return"["+e+" "+a+t.id+"]"},topicPrefix:function(t){if("topics"==t.type)return"";var e=t.repo,a="pull"==t.type?"PR":"#";return"["+e+" "+a+t.id+"]"}}},c=u,p=(a("d747"),a("2877")),m=Object(p["a"])(c,n,i,!1,null,"738bef65",null),d=m.exports,f={name:"app",components:{SideBar:d}},b=f,h=(a("9062"),Object(p["a"])(b,r,o,!1,null,"0fbf8216",null)),v=h.exports,_=a("8c4f"),g=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},[a("p",[t._v("dashboard")]),a("b-card",{attrs:{title:"Message 1"}},[a("b-card-text",[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])],1),a("b-card",{attrs:{title:"Message 2"}},[a("b-card-text",[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])],1),a("b-card",{attrs:{title:"Message 3"}},[a("b-card-text",[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])],1)],1)},w=[],y={name:"DashBoard",data:function(){return{}}},x=y,C=(a("8e53"),Object(p["a"])(x,g,w,!1,null,"8c6a53ae",null)),k=C.exports,S=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"dashboard"},[s("RepoNav"),s("div",{staticStyle:{padding:"0.2rem 1rem 0.2rem 1rem"}},[t._v("descriptions")]),s("b-nav",{staticClass:"border rounded",staticStyle:{padding:"0.2rem 0"},attrs:{pills:"",fill:""}},[s("b-nav-item",[s("router-link",{staticClass:"nav-link",attrs:{to:"#"}},[t._v(t._s(t.commitNumber)+" commits")])],1),s("b-nav-item",[s("router-link",{staticClass:"nav-link",attrs:{to:"#"}},[t._v(t._s(t.branchNumber)+" branches")])],1),s("b-nav-item",[s("router-link",{staticClass:"nav-link",attrs:{to:"#"}},[t._v(t._s(t.releaseNumber)+" releases")])],1),s("b-nav-item",[s("router-link",{staticClass:"nav-link",attrs:{to:"#"}},[t._v(t._s(t.contributorNumber)+" contributors")])],1),s("b-nav-item",[s("router-link",{staticClass:"nav-link",attrs:{to:"#"}},[t._v("View lisence")])],1)],1),s("b-row",{staticStyle:{"white-space":"nowrap","overflow-x":"hidden"}},[s("div",[s("b-dropdown",{staticClass:"col-2",attrs:{variant:"info",boundary:"window",size:"sm",text:"Branch: "+t.currentBranch}},t._l(t.branches,function(e){return s("b-dropdown-item",{key:e},[t._v(t._s(e))])}),1)],1),s("b-col",{attrs:{cols:"2"}},[s("button",{staticClass:"d-none d-md-inline-block btn btn-sm btn-secondary",attrs:{type:"button"},on:{click:function(e){return e.preventDefault(),t.newPull(e)}}},[t._v("New pull request")])]),s("b-col",{staticStyle:{overflow:"hidden"},attrs:{cols:"3",offset:"3"}},[s("b-btn-group",{staticClass:"-md-inline-flex"},[s("b-button",{attrs:{variant:"secondary",size:"sm"}},[t._v("Create new file")]),s("b-button",{attrs:{variant:"secondary",size:"sm"}},[t._v("Upload files")]),s("b-button",{attrs:{variant:"secondary",size:"sm"}},[t._v("Find file")])],1),t._v(" \n    ")],1),s("div",{staticClass:"clone"},[s("b-dropdown",{staticClass:"col-2",attrs:{variant:"success",boundary:"window",right:"",size:"sm",text:"Clone or download"}},[s("b-dropdown-item",{on:{click:function(e){return e.preventDefault(),t.clone(e)}}},[t._v("Clone: http://gapsule.com/"+t._s(t.$route.params.owner)+"/"+t._s(t.$route.params.repo)+".git")]),s("b-dropdown-item",{on:{click:function(e){return e.preventDefault(),t.download(e)}}},[t._v("Download Zip")])],1)],1)],1),s("b-card",{staticClass:"filelist",attrs:{"no-body":""}},[s("b-card-header",[t._v("file list")]),s("b-list-group",{attrs:{flush:""}},[t._l(t.files["folder"],function(e){return s("b-list-group-item",{key:e},[s("img",{attrs:{src:a("e8b1")}}),s("router-link",{attrs:{to:t.fullRepoName()+"/tree/"+t.currentBranch+"/"+e}},[t._v(t._s(e))])],1)}),t._l(t.files["file"],function(e){return s("b-list-group-item",{key:e},[s("img",{attrs:{src:a("626e")}}),s("router-link",{attrs:{to:t.fullRepoName()+"/blob/"+t.currentBranch+"/"+e}},[t._v(t._s(e))])],1)})],2)],1),s("b-card",{attrs:{"no-body":""}},[s("b-card-header",[t._v("readme")]),s("b-card-body",[t._v(t._s(t.readme))])],1)],1)},N=[],$=(a("a481"),function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"reponav"},[a("div",{staticClass:"bg-light",staticStyle:{padding:"0 1%"}},[a("h4",{staticStyle:{padding:"0.5rem 2%"}},[a("router-link",{attrs:{to:"/"+t.$route.params.owner}},[t._v(t._s(t.$route.params.owner))]),a("strong",[t._v("/")]),a("router-link",{attrs:{to:"/"+t.fullRepoName()}},[t._v(t._s(t.$route.params.repo))])],1),a("b-nav",{attrs:{tabs:""}},[a("b-nav-item",{attrs:{active:"Repo"==t.$route.name||"PullCompare"==t.$route.name,to:"/"+t.fullRepoName()}},[t._v("Code")]),a("b-nav-item",{attrs:{active:"Issues"==t.$route.name,to:"/"+t.fullRepoName()+"/issues"}},[t._v("Issues")]),a("b-nav-item",{attrs:{active:"PullRequest"==t.$route.name||"PullConversion"==t.$route.name||"PullCommits"==t.$route.name,to:"/"+t.fullRepoName()+"/pull"}},[t._v("Pull request")])],1)],1)])}),A=[],P={name:"Profile",data:function(){return{msg:"Welcome to Your Vue.js App"}},methods:{fullRepoName:function(){return this.$route.params.owner+"/"+this.$route.params.repo}}},I=P,E=(a("f203"),Object(p["a"])(I,$,A,!1,null,"b9e2138a",null)),R=E.exports,j=a("bc3a"),O=a.n(j),T=a("9323"),D=a.n(T),U={name:"Profile",data:function(){return{commitNumber:"",branchNumber:"",releaseNumber:"",contributorNumber:"",currentBranch:"",branches:{},files:{},readme:"",msg:"Welcome to Your Vue.js App"}},created:function(){this.getData()},watch:{$route:"getData"},methods:{fullRepoName:function(){return"/"+this.$route.params.owner+"/"+this.$route.params.repo},newPull:function(){this.$router.replace(this.fullRepoName()+"/compare")},getData:function(){var t=this,e=new D.a(O.a);e.onGet(this.fullRepoName()).reply(200,{state:"ok",error:"error",commitNumber:1,branchNumber:2,releaseNumber:3,contributorNumber:4,readme:"readme",files:{folder:["folder1","folder2"],file:["file1","file2"]},currentBranch:"master",branches:["master"]}),O()({method:"GET",url:this.fullRepoName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo}}).then(function(e){"ok"==e.data.state?(t.commitNumber=e.data.commitNumber,t.branchNumber=e.data.branchNumber,t.releaseNumber=e.data.releaseNumber,t.contributorNumber=e.data.contributorNumber,t.readme=e.data.readme,t.files=e.data.files,t.currentBranch=e.data.currentBranch,t.branches=e.data.branches):console.log(e.data.error)})}},components:{RepoNav:R}},B=U,G=(a("7e75"),Object(p["a"])(B,S,N,!1,null,"516f7576",null)),q=G.exports,z=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("div",[a("span",{staticStyle:{"font-weight":"400","font-size":"32px"}},[t._v(t._s(t.topic))]),t._v("  \n    "),a("span",{staticStyle:{"font-weight":"300","font-size":"32px",color:"#a3aab1"}},[t._v("#"+t._s(t.$route.params.issueid))]),a("p",[t.isOpen?a("b-badge",{attrs:{variant:"success",disabled:"",size:"sm"}},[t._v("Opened")]):a("b-badge",{attrs:{variant:"danger",disabled:"",size:"sm"}},[t._v("Closed")]),t._v("\n       \n      "+t._s(t.issueCreator)+" opened this issue "+t._s(t.date)+" · "+t._s(t.commetsNumber)+" comments\n    ")],1)]),t._l(t.replys,function(e){return a("b-card",{key:e,staticStyle:{width:"60%"},attrs:{"no-body":"",header:"commetInfo","header-tag":"header"}},[a("router-link",{staticStyle:{color:"#656d74"},attrs:{slot:"header",to:"/"+e.user},slot:"header"},[a("strong",[t._v(t._s(e.user))]),t._v(" \n    ")]),a("span",{attrs:{slot:"header"},slot:"header"},[t._v("commented "+t._s(e.date))]),a("b-card-body",[a("p",{staticClass:"card-text"},[t._v(t._s(e.text))])])],1)}),a("b-card",{staticStyle:{width:"60%"}},[a("b-form",[a("b-form-textarea",{staticStyle:{"margin-bottom":"10px"},attrs:{placeholder:"Leave a commet",size:"md",rows:"5","max-rows":"10"},model:{value:t.comments,callback:function(e){t.comments=e},expression:"comments"}}),a("div",{staticStyle:{float:"right"}},[t.show?[t.isOpen?a("b-button",{attrs:{type:"submit"},on:{click:function(e){return e.preventDefault(),t.closeIssue(e)}}},[t._v("Close Issue")]):a("b-button",{attrs:{type:"submit"},on:{click:function(e){return e.preventDefault(),t.reopenIssue(e)}}},[t._v("Reopen Issue")])]:t._e(),a("b-button",{staticStyle:{"margin-left":"5px"},attrs:{variant:"success",type:"submit"},on:{click:function(e){return e.preventDefault(),t.comment(e)}}},[t._v("Comment")])],2)],1)],1)],2)},F=[],M={data:function(){return{topic:"",issueCreator:"",date:"",commetsNumber:"",replys:[],comments:"",show:!0,isOpen:!0}},created:function(){this.getData()},watch:{$route:"getData"},methods:{fullIssueName:function(){var t=this.$route.params;return"/"+t.owner+"/"+t.repo+"/issues/"+t.issueid},closeIssue:function(){this.isOpen=!1,O()({method:"GET",url:this.fullIssueName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.issueid,action:"closeIssue"}}).then(function(t){"ok"==t.data.state?console.log("this issue is closed"):console.log(t.data.error)})},reopenIssue:function(){this.isOpen=!0,O()({method:"GET",url:this.fullIssueName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.issueid,action:"reopenIssue"}}).then(function(t){"ok"==t.data.state?console.log("this issue is opend"):console.log(t.data.error)})},comment:function(){var t=this;O()({method:"GET",url:this.fullIssueName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.issueid,comments:this.comments}}).then(function(e){if("ok"==e.data.state){var a={};a["user"]=e.data.user,a["date"]="just now",a["text"]=t.comments,t.replys.push(a),t.comments=""}else console.log(e.data.error)})},getData:function(){var t=this;O()({method:"GET",url:this.fullIssueName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.issueid}}).then(function(e){var a;if("ok"==e.data.state)for(a in t.topic=e.data.topic,t.issueCreator=e.data.issueCreator,t.date=e.data.date,t.commetsNumber=e.data.commetsNumber,t.show=e.data.show,t.isOpen=e.data.isOpen,e.data.replys)t.replys.push(e.data.replys[a]);else console.log(e.data.error)})}},components:{RepoNav:R}},V=M,J=(a("3b79"),Object(p["a"])(V,z,F,!1,null,"3bdf826e",null)),L=J.exports,Y=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"login"}},[t._m(0),a("h2",{staticStyle:{"text-align":"center"}},[t._v("Sign in to Gapsule")]),a("b-form",{on:{submit:t.onSubmit}},[a("ul",{staticClass:"main"},[a("li",{staticClass:"username"},[a("label",{attrs:{for:"username"}},[t._v("Username")]),a("b-form-input",{attrs:{id:"username",type:"text",required:"",placeholder:"Enter Username"},model:{value:t.username,callback:function(e){t.username=e},expression:"username"}})],1),a("li",{staticClass:"password"},[a("label",{attrs:{for:"password"}},[t._v("Password")]),a("a",{staticStyle:{float:"right"},attrs:{href:"#"}},[t._v("Forget Password?")]),a("b-form-input",{attrs:{id:"password",type:"password",required:"",placeholder:"Enter password"},model:{value:t.password,callback:function(e){t.password=e},expression:"password"}})],1),a("li",{staticClass:"operation"},[a("b-button",{staticClass:"submit",attrs:{block:"",type:"submit",variant:"primary"}},[t._v("Submit")])],1)])]),a("div",{staticClass:"create-account"},[a("span",[t._v("New to Gapsule?")]),a("router-link",{attrs:{to:"/signup"}},[t._v("Create an account")])],1)],1)},W=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"logo"},[s("img",{attrs:{src:a("c046"),alt:"Logo"}})])}],Q={name:"SignIn",data:function(){return{username:"",password:""}},methods:{onSubmit:function(){var t=this;O()({method:"POST",url:"/signin",data:{ajax:1,username:this.username,password:this.password}}).then(function(e){200==e.status&&t.$router.replace("/index")})}}},H=Q,K=(a("a07b"),Object(p["a"])(H,Y,W,!1,null,"689dc7ac",null)),Z=K.exports,X=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"signup"}},[a("h2",{staticStyle:{"text-align":"center"}},[t._v("Join Gapsule")]),a("b-form",{on:{submit:function(e){return e.preventDefault(),t.onSubmit(e)}}},[a("ul",{staticClass:"main"},[a("span",{staticStyle:{color:"red"}},[t._v(t._s(t.errormessage))]),a("li",{staticClass:"username"},[a("label",{attrs:{for:"username"}},[t._v("Username")]),a("span",{staticStyle:{color:"red"}},[t._v("*")]),a("b-form-input",{attrs:{id:"username",type:"text",required:"",placeholder:"Enter Username"},model:{value:t.username,callback:function(e){t.username=e},expression:"username"}})],1),a("li",{staticClass:"email"},[a("label",{attrs:{for:"email"}},[t._v("Email")]),a("span",{staticStyle:{color:"red"}},[t._v("*")]),a("b-form-input",{attrs:{id:"email",type:"email",required:"",placeholder:"Enter Email"},model:{value:t.email,callback:function(e){t.email=e},expression:"email"}})],1),a("li",{staticClass:"password"},[a("label",{attrs:{for:"password"}},[t._v("Password")]),a("span",{staticStyle:{color:"red"}},[t._v("*")]),a("b-input",{attrs:{id:"password",required:"",state:t.validation,type:"password",placeholder:"Enter Password"},model:{value:t.password,callback:function(e){t.password=e},expression:"password"}}),a("b-form-invalid-feedback",{attrs:{state:t.validation}},[t._v("Your password must be 6-18 characters long")]),a("b-form-valid-feedback",{attrs:{state:t.validation}},[t._v("Looks good")])],1),a("li",{staticClass:"operation"},[a("b-button",{staticClass:"submit",attrs:{block:"",type:"submit",variant:"primary"}},[t._v("Next")])],1)])])],1)},tt=[],et={name:"SignUp",data:function(){return{username:"",email:"",password:"",password_entered:!1,errormessage:""}},methods:{onSubmit:function(){var t=this;O()({method:"POST",url:"/signup",data:{ajax:1,username:this.username,email:this.email,password:this.password}}).then(function(e){"ok"==e.data.state?t.$router.replace("/signup/verify"):t.errormessage=e.data.error}).catch(function(t){console.log(t)})}},computed:{validation:function(){return this.password_entered||0!=this.password.length?(this.password_entered=!0,this.password.length>=6&&this.password.length<=18):null}}},at=et,st=(a("fc4b"),Object(p["a"])(at,X,tt,!1,null,"55543185",null)),rt=st.exports,ot=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"login"}},[a("h3",{staticStyle:{"text-align":"center"}},[t._v("Vertify your password")]),a("b-form",{on:{submit:function(e){return e.preventDefault(),t.onSubmit(e)}}},[a("ul",{staticClass:"main"},[a("li",{staticClass:"username"},[a("label",{attrs:{for:"username"}},[t._v("Username")]),a("b-form-input",{attrs:{id:"username",type:"text",disabled:"",placeholder:t.username}})],1),a("li",{staticClass:"password"},[a("label",{attrs:{for:"password"}},[t._v("Password")]),a("b-form-input",{attrs:{id:"password",type:"password",required:"",placeholder:"Enter password"},model:{value:t.password,callback:function(e){t.password=e},expression:"password"}})],1),a("li",{staticClass:"operation"},[a("b-button",{staticClass:"submit",attrs:{type:"submit",variant:"primary"}},[t._v("Submit")])],1)])])],1)},nt=[],it={name:"SignupVerify",data:function(){return{username:"",password:""}},created:function(){this.fetchUsername()},watch:{$route:"fetchUsername"},methods:{onSubmit:function(){var t=this;O()({method:"POST",url:"/signup/verify",data:{ajax:1,password:this.password}}).then(function(e){"ok"==e.data.state&&t.$router.replace("/signup/finishing")})},fetchUsername:function(){var t=this;O()({method:"POST",url:"/signup/verify",data:{ajax:1}}).then(function(e){"ok"==e.data.state?(console.log(e.data.username),t.username=e.data.username):console.log(e.data.error)})}}},lt=it,ut=(a("305d"),Object(p["a"])(lt,ot,nt,!1,null,"79096be0",null)),ct=ut.exports,pt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"userinfo"}},[a("h4",{staticStyle:{"text-align":"center",padding:"10px 0"}},[t._v("Fill in your information")]),a("b-form",{on:{submit:function(e){return e.preventDefault(),t.onSubmit(e)}}},[a("ul",{staticClass:"main"},[a("li",{staticClass:"icon"},[a("label",{attrs:{for:"icon"}},[t._v("Choose an image as your icon")]),a("img",{attrs:{src:t.icon,alt:"User Icon",id:"icon"}}),a("input",{ref:"icon",attrs:{id:"choose",type:"file",name:"icon",accept:"image/*"},on:{change:function(e){return t.changeImg(e)}}})]),a("li",{staticClass:"name"},[a("b-form-group",{staticClass:"fullname",attrs:{label:"Name","label-for":"firstname",horizontal:""}},[a("b-row",[a("b-col",{attrs:{cols:"6"}},[a("b-form-input",{attrs:{id:"firstname",type:"text",placeholder:"firstname",required:""},model:{value:t.firstname,callback:function(e){t.firstname=e},expression:"firstname"}})],1),a("b-col",{attrs:{cols:"6"}},[a("b-form-input",{attrs:{id:"secondname",type:"text",placeholder:"secondname",required:""},model:{value:t.secondname,callback:function(e){t.secondname=e},expression:"secondname"}})],1)],1)],1)],1),a("li",{staticClass:"biography"},[a("label",{attrs:{for:"biography"}},[t._v("Biography")]),a("b-form-input",{attrs:{id:"biography",type:"text"},model:{value:t.biography,callback:function(e){t.biography=e},expression:"biography"}})],1),a("li",{staticClass:"company"},[a("label",{attrs:{for:"company"}},[t._v("Company")]),a("b-form-input",{attrs:{id:"company",type:"text"},model:{value:t.company,callback:function(e){t.company=e},expression:"company"}})],1),a("li",{staticClass:"location"},[a("label",{attrs:{for:"location"}},[t._v("Location")]),a("b-form-input",{attrs:{id:"location",type:"text"},model:{value:t.location,callback:function(e){t.location=e},expression:"location"}})],1),a("li",{staticClass:"website"},[a("label",{attrs:{for:"website"}},[t._v("Website")]),a("b-form-input",{attrs:{id:"website",type:"text"},model:{value:t.website,callback:function(e){t.website=e},expression:"website"}})],1),a("li",{staticClass:"operation"},[a("b-button",{staticClass:"submit",attrs:{type:"submit",variant:"primary"}},[t._v("Submit")])],1)])])],1)},mt=[],dt={name:"SignupFinishing",data:function(){return{icon:a("5444"),firstname:"",secondname:"",biography:"",company:"",location:"",website:""}},methods:{changeImg:function(t){var e=t.target.files[0],a=new FileReader,s=this;a.readAsDataURL(e),a.onload=function(){s.icon=this.result}},onSubmit:function(t){var e=this;t.preventDefault(),O()({method:"POST",url:"/signup/finishing",data:{ajax:1,icon:this.icon,firstname:this.firstname,secondname:this.secondname,biography:this.biography,company:this.company,location:this.location,website:this.website}}).then(function(t){"ok"==t.data.state?e.$router.replace("/index"):console.log(t.data.error)}).catch(function(t){console.log(t)})}}},ft=dt,bt=(a("a021"),a("9298"),Object(p["a"])(ft,pt,mt,!1,null,"5ad16437",null)),ht=bt.exports,vt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("b-row",[a("b-col",{attrs:{cols:"4"}},[t.isIssuePage?a("b-form-input",{attrs:{placeholder:"Search issues"},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.getSearchDatas(e)}}}):a("b-form-input",{attrs:{placeholder:"Search Pulls"},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.getSearchDatas(e)}}})],1),a("b-col",{attrs:{cols:"2",offset:"6"}},[a("b-button",{attrs:{block:"",variant:"success"},on:{click:t.newIssue}},[t._v("New "+t._s(t.operateType))])],1)],1),t._l(t.issues,function(e){return a("b-card",{key:e,attrs:{"no-body":""}},[a("b-card-body",[a("router-link",{attrs:{to:t.fullIssuesName()+"/"+e.id}},[a("h5",{staticClass:"card-title"},[t._v(t._s(e.topic))])]),a("p",{staticClass:"card-text"},[t._v(t._s("#"+e.id+" opened on "+e.date+" by "+e.user))])],1)],1)})],2)},_t=[],gt={props:{isIssuePage:{type:Boolean},operateType:{validator:function(t){return-1!==["issues","pull"].indexOf(t)}}},data:function(){return{issues:""}},created:function(){this.getIssues()},watch:{$route:"getIssues"},methods:{fullIssuesName:function(){var t=this.$route.params;return"/"+t.owner+"/"+t.repo+"/"+this.operateType},getIssues:function(){var t=this;O()({method:"GET",url:this.fullIssuesName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo}}).then(function(e){"ok"==e.data.state?t.issues=e.data.issues:console.log(e.data.error)})},getSearchDatas:function(){this.getIssues()},newIssue:function(){if(this.isIssuePage)this.$router.replace(this.fullIssuesName()+"/new");else{var t=this.$route.params;this.$router.replace("/"+t.owner+"/"+t.repo+"/compare")}}},components:{RepoNav:R}},wt=gt,yt=(a("e5ca"),Object(p["a"])(wt,vt,_t,!1,null,"44393b1c",null)),xt=yt.exports,Ct=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("b-card",{staticStyle:{width:"60%"}},[a("b-form",{on:{submit:function(e){return e.preventDefault(),t.onSubmit(e)}}},[a("b-form-input",{staticStyle:{"margin-bottom":"10px"},attrs:{placeholder:"Title",required:""},model:{value:t.title,callback:function(e){t.title=e},expression:"title"}}),a("b-form-textarea",{staticStyle:{"margin-bottom":"10px"},attrs:{placeholder:"Leave a commet",size:"md",rows:"5","max-rows":"10"},model:{value:t.commet,callback:function(e){t.commet=e},expression:"commet"}}),a("b-button",{staticStyle:{float:"right"},attrs:{variant:"success",type:"submit"}},[t._v("Submit new issue")])],1)],1)],1)},kt=[],St={name:"Issues",data:function(){return{title:"",commet:""}},methods:{fullIssuesName:function(){var t=this.$route.params;return"/"+t.owner+"/"+t.repo+"/issues"},onSubmit:function(){var t=this;O()({method:"GET",url:this.fullIssuesName()+"/new",params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,title:this.title,commet:this.commet}}).then(function(e){"ok"==e.data.state?t.$router.replace(t.fullIssuesName()+"/"+e.data.issueid):console.log(e.data.error)})}},components:{RepoNav:R}},Nt=St,$t=(a("d768"),Object(p["a"])(Nt,Ct,kt,!1,null,"b63615a0",null)),At=$t.exports,Pt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("h4",[t._v("Compare changes")]),a("p",[t._v("Compare changes across branches, commits, tags, and more below.")])],1)},It=[],Et={components:{RepoNav:R}},Rt=Et,jt=(a("9921"),Object(p["a"])(Rt,Pt,It,!1,null,"8f110754",null)),Ot=jt.exports,Tt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("div",[a("span",{staticStyle:{"font-weight":"400","font-size":"32px"}},[t._v(t._s(t.topic))]),t._v("  \n    "),a("span",{staticStyle:{"font-weight":"300","font-size":"32px",color:"#a3aab1"}},[t._v("#"+t._s(t.$route.params.pullid))]),a("div",["open"==t.pullState?a("p",[a("b-badge",{attrs:{variant:"success"}},[t._v("Open")]),t._v("\n        "+t._s(t.pullUser)+" wants to merge "+t._s(t.commitsNumber)+" commits into "+t._s(t.pullTo)+" from "+t._s(t.pullFrom)+"\n      ")],1):a("p",[a("b-badge",{attrs:{variant:"info"}},[t._v("Merged")]),t._v("\n        "+t._s(t.pullUser)+" merged asdfaadsfa "+t._s(t.commitsNumber)+" commits into "+t._s(t.pullTo)+" from "+t._s(t.pullFrom)+"\n      ")],1)])]),a("b-nav",{attrs:{tabs:""}},[a("b-nav-item",{attrs:{active:"PullConversion"==t.$route.name,to:t.fullPullName()}},[t._v("Conversion")]),a("b-nav-item",{attrs:{active:"PullCommits"==t.$route.name,to:t.fullPullName()+"/commits"}},[t._v("Commits")])],1),t._l(t.replys,function(e){return a("b-card",{key:e,staticStyle:{width:"60%"},attrs:{"no-body":"",header:"commetInfo","header-tag":"header"}},[a("router-link",{staticStyle:{color:"#656d74"},attrs:{slot:"header",to:"/"+e.user},slot:"header"},[a("strong",[t._v(t._s(e.user))]),t._v(" \n    ")]),a("span",{attrs:{slot:"header"},slot:"header"},[t._v("commented "+t._s(e.date))]),a("b-card-body",[a("p",{staticClass:"card-text"},[t._v(t._s(e.text))])])],1)}),a("b-card",{staticStyle:{width:"60%"}},[a("b-form",[a("b-form-textarea",{staticStyle:{"margin-bottom":"10px"},attrs:{placeholder:"Leave a commet",size:"md",rows:"5","max-rows":"10"},model:{value:t.comments,callback:function(e){t.comments=e},expression:"comments"}}),a("div",{staticStyle:{float:"right"}},[a("b-button",{attrs:{variant:"success",type:"submit"},on:{click:function(e){return e.preventDefault(),t.comment(e)}}},[t._v("Comment")])],1)],1)],1)],2)},Dt=[],Ut={data:function(){return{topic:"",pullState:"",pullUser:"",commitsNumber:"",pullTo:"",pullFrom:"",replys:[],comments:""}},created:function(){this.getData()},watch:{$route:"getData"},methods:{fullPullName:function(){var t=this.$route.params;return"/"+t.owner+"/"+t.repo+"/pull/"+t.pullid},comment:function(){var t=this;O()({method:"GET",url:this.fullPullName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.pullid,comments:this.comments}}).then(function(e){if("ok"==e.data.state){var a={};a["user"]=e.data.user,a["date"]="just now",a["text"]=t.comments,t.replys.push(a),t.comments=""}else console.log(e.data.error)})},getData:function(){var t=this;O()({method:"GET",url:this.fullPullName(),params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.pullid}}).then(function(e){var a;if("ok"==e.data.state)for(a in t.topic=e.data.topic,t.pullState=e.data.pullState,t.pullUser=e.data.pullUser,t.commitsNumber=e.data.commitsNumber,t.pullTo=e.data.pullTo,t.pullFrom=e.data.pullFrom,e.data.replys)t.replys.push(e.data.replys[a]);else console.log(e.data.error)})}},components:{RepoNav:R}},Bt=Ut,Gt=(a("b963"),Object(p["a"])(Bt,Tt,Dt,!1,null,"95d499f2",null)),qt=Gt.exports,zt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("div",[a("span",{staticStyle:{"font-weight":"400","font-size":"32px"}},[t._v(t._s(t.topic))]),t._v("  \n    "),a("span",{staticStyle:{"font-weight":"300","font-size":"32px",color:"#a3aab1"}},[t._v("#"+t._s(t.$route.params.pullid))]),a("div",["open"==t.pullState?a("div",[a("b-badge",{attrs:{variant:"success"}},[t._v("Open")]),a("span",[t._v(t._s(t.pullUser)+" wants to merge "+t._s(t.commitsNumber)+" commits into "+t._s(t.pullTo)+" from "+t._s(t.pullFrom))])],1):a("div",[a("b-badge",{attrs:{variant:"info"}},[t._v("Merged")]),a("span",[t._v(t._s(t.pullUser)+" merged "+t._s(t.commitsNumber)+" commits into "+t._s(t.pullTo)+" from "+t._s(t.pullFrom))])],1)])]),a("b-nav",{attrs:{tabs:""}},[a("b-nav-item",{attrs:{active:"PullConversion"==t.$route.name,to:t.fullPullName()}},[t._v("Conversion")]),a("b-nav-item",{attrs:{active:"PullCommits"==t.$route.name,to:t.fullPullName()+"/commits"}},[t._v("Commits")])],1),t._l(t.replys,function(e){return a("div",{key:e},[a("span",[t._v("Commits on "+t._s(e.commitsDate))]),a("div",{staticStyle:{"background-color":"#f5fcff","margin-left":"1%","margin-top":"5px"}},[a("strong",[t._v(t._s(e.title))]),a("p",[t._v(t._s(e.user)+" committed "+t._s(e.timeToNow))])])])})],2)},Ft=[],Mt={data:function(){return{topic:"",pullState:"",pullUser:"",commitsNumber:"",pullTo:"",pullFrom:"",replys:""}},beforeRouteEnter:function(t,e,a){a(function(t){return t.getData()})},beforeRouteUpdate:function(t,e,a){this.getData(),a()},methods:{fullPullName:function(){var t=this.$route.params;return"/"+t.owner+"/"+t.repo+"/pull/"+t.pullid},getData:function(){var t=this;O()({method:"GET",url:this.fullPullName()+"/commits",params:{ajax:1,owner:this.$route.params.owner,repo:this.$route.params.repo,id:this.$route.params.pullid}}).then(function(e){"ok"==e.data.state?(t.topic=e.data.topic,t.pullState=e.data.pullState,t.pullUser=e.data.pullUser,t.commitsNumber=e.data.commitsNumber,t.pullTo=e.data.pullTo,t.pullFrom=e.data.pullFrom,t.replys=e.data.replys):console.log(e.data.error)})}},components:{RepoNav:R}},Vt=Mt,Jt=(a("d998"),Object(p["a"])(Vt,zt,Ft,!1,null,"68fc3430",null)),Lt=Jt.exports;s["default"].use(_["a"]);var Yt=new _["a"]({mode:"history",routes:[{path:"/signin",name:"SignIn",component:Z,meta:{title:"SignIn"}},{path:"/signup",name:"SignUp",component:rt,meta:{title:"Join Gapsule"}},{path:"/signup/verify",name:"SignupVerify",component:ct,meta:{title:"Signup Verify"}},{path:"/signup/finishing",name:"SignupFinishing",component:ht,meta:{title:"Signup Finishing"}},{path:"/",name:"DashBoard",component:k},{path:"/:owner/:repo",name:"Repo",component:q,meta:function(){return this.params.owner+"/"+this.params.repo}},{path:"/topics/:title",name:"Topic",component:L,meta:function(){return this.params.title}},{path:"/:owner/:repo/issues",name:"Issues",component:xt,props:{isIssuePage:!0,operateType:"issues"},meta:function(){return"Issues "+this.params.owner+"/"+this.params.repo}},{path:"/:owner/:repo/issues/new",name:"Issues",component:At,meta:function(){return"New Issues · "+this.params.owner+"/"+this.params.repo}},{path:"/:owner/:repo/issues/:issueid",name:"Issues",component:L,meta:function(){return"Issues "+this.params.owner+"/"+this.params.repo+"/"+this.params.issueid}},{path:"/:owner/:repo/pull",name:"PullRequest",component:xt,props:{isIssuePage:!1,operateType:"pull"},meta:function(){return"PullRequest · "+this.params.owner+"/"+this.params.repo}},{path:"/:owner/:repo/compare",name:"PullCompare",component:Ot,meta:function(){return"Compare · "+this.params.owner+"/"+this.params.repo}},{path:"/:owner/:repo/pull/:pullid",name:"PullConversion",component:qt,meta:function(){return"PullRequest · "+this.params.owner+"/"+this.params.repo+"/"+this.params.pullid}},{path:"/:owner/:repo/pull/:pullid/commits",name:"PullCommits",component:Lt,meta:function(){return"PullRequest · "+this.params.owner+"/"+this.params.repo+"/"+this.params.pullid+"/commits"}}]}),Wt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-navbar",{staticClass:"bg-dark",attrs:{toggleable:"lg",type:"dark"}},[a("b-navbar-brand",{attrs:{to:"/"}},[t._v("Gapsule")]),a("b-navbar-toggle",{attrs:{id:"navbar-toggler",target:"navbarSupportedContent"}},[a("span",{staticClass:"navbar-toggler-icon"})]),a("b-collapse",{attrs:{id:"navbarSupportedContent","is-nav":""}},[a("b-navbar-nav",{staticClass:"mr-auto"},[a("b-nav-item",{attrs:{active:"",to:"#"}},[t._v("\n        Home\n        "),a("span",{staticClass:"sr-only"},[t._v("(current)")])]),a("b-nav-item",{attrs:{to:"#"}},[t._v("Link")]),a("b-nav-item-dropdown",{attrs:{text:"Dropdown"}},[a("b-dropdown-item",{attrs:{to:"#"}},[t._v("Action")]),a("b-dropdown-item",{attrs:{to:"#"}},[t._v("Another action")]),a("b-dropdown-divider"),a("b-dropdown-item",{attrs:{to:"#"}},[t._v("Something else here")])],1),a("b-nav-item",{attrs:{to:"#"}},[t._v("Disabled")])],1),a("b-navbar-nav",{staticClass:"ml-auto"},[a("b-nav-form",[a("b-form-input",{staticClass:"mr-sm-2",attrs:{size:"sm",type:"search",placeholder:"Search","aria-label":"Search"}}),a("b-button",{staticClass:"my-2 my-sm-0",attrs:{variant:"outline-success",size:"sm"}},[t._v("Search")])],1),t._v("  \n      "),a("b-nav-item",{staticStyle:{color:"white"},attrs:{to:"/signin"}},[t._v("Sign in")]),t._v("  \n      "),a("b-nav-form",[a("b-button",{staticClass:"my-2 my-sm-0",attrs:{to:"/signup",size:"sm"}},[t._v("Sign Up")])],1)],1)],1)],1)},Qt=[],Ht={name:"NavBar",mounted:function(){}},Kt=Ht,Zt=(a("b945"),Object(p["a"])(Kt,Wt,Qt,!1,null,"57398480",null)),Xt=Zt.exports,te=a("9f7b"),ee=a.n(te),ae=(a("f9e3"),a("2dd8"),a("5c96"));s["default"].use(ee.a),s["default"].use(ae["Steps"]),s["default"].config.productionTip=!1;var se="Gapsule";Yt.afterEach(function(t,e){"function"==typeof t.meta?document.title=t.meta.call(t)||se:document.title=t.meta.title||se}),new s["default"]({router:Yt,render:function(t){return t(v)}}).$mount("#app"),new s["default"]({router:Yt,render:function(t){return t(Xt)}}).$mount("#navbar")},"575a":function(t,e,a){},"626e":function(t,e){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAeCAYAAAA/xX6fAAAAuUlEQVRIiWP8DwQMdARM9LRs1MJRC0ctxApYiFE0ZfkuhudvPuCUF+DlYkgPcWbg4+EkbNh/IkDVpJV45feeuPK/a/7m/x8/fyNoFlWC1Mlcm0FXVZZh5pq9DJ++fMerlqgghYHqyatQ+K25YXC2h7U+mAZZWprgQx0LkS3ABkCWHj53E6+awZlKYQA9SJEBId+TZSGxhlLNwlEfUt1CavhwcGYLSREBvMGJrhYfYBxtJo5aOGohOgAAfQaa2kHoBCMAAAAASUVORK5CYII="},"69cd":function(t,e,a){},"6cb3":function(t,e,a){},"7e75":function(t,e,a){"use strict";var s=a("fec6"),r=a.n(s);r.a},8728:function(t,e,a){},"8e53":function(t,e,a){"use strict";var s=a("e540"),r=a.n(s);r.a},9062:function(t,e,a){"use strict";var s=a("575a"),r=a.n(s);r.a},9298:function(t,e,a){"use strict";var s=a("3a69"),r=a.n(s);r.a},9921:function(t,e,a){"use strict";var s=a("36fc"),r=a.n(s);r.a},a021:function(t,e,a){"use strict";var s=a("3b02"),r=a.n(s);r.a},a07b:function(t,e,a){"use strict";var s=a("b548"),r=a.n(s);r.a},b548:function(t,e,a){},b945:function(t,e,a){"use strict";var s=a("bded"),r=a.n(s);r.a},b963:function(t,e,a){"use strict";var s=a("8728"),r=a.n(s);r.a},bded:function(t,e,a){},c046:function(t,e,a){t.exports=a.p+"static/img/logo.d54f0884.jpg"},d747:function(t,e,a){"use strict";var s=a("329f"),r=a.n(s);r.a},d768:function(t,e,a){"use strict";var s=a("69cd"),r=a.n(s);r.a},d998:function(t,e,a){"use strict";var s=a("6cb3"),r=a.n(s);r.a},e540:function(t,e,a){},e5ca:function(t,e,a){"use strict";var s=a("31e0"),r=a.n(s);r.a},e8b1:function(t,e){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAeCAYAAAA/xX6fAAAAgklEQVRIiWP8DwQMdARM9LRs1MJRC0ctHBwWshCjaPbafQxvPnzGEJcWE2KI87WlvoUgyyqT/THE2+duJMkyEGAkpiwlx2ARAV6G1GAnDHGaxSG2KKCphbjAqIVD28IfP37S10IODvZBGqSignwkG4xLD1ElDTXB4AzSUQtHLRxQCwH/gyE4mPm/XwAAAABJRU5ErkJggg=="},f203:function(t,e,a){"use strict";var s=a("4473"),r=a.n(s);r.a},f6f5:function(t,e,a){},fc4b:function(t,e,a){"use strict";var s=a("f6f5"),r=a.n(s);r.a},fec6:function(t,e,a){}});
//# sourceMappingURL=app.b84f38d5.js.map