(function(t){function e(e){for(var r,o,i=e[0],l=e[1],c=e[2],p=0,d=[];p<i.length;p++)o=i[p],s[o]&&d.push(s[o][0]),s[o]=0;for(r in l)Object.prototype.hasOwnProperty.call(l,r)&&(t[r]=l[r]);u&&u(e);while(d.length)d.shift()();return n.push.apply(n,c||[]),a()}function a(){for(var t,e=0;e<n.length;e++){for(var a=n[e],r=!0,i=1;i<a.length;i++){var l=a[i];0!==s[l]&&(r=!1)}r&&(n.splice(e--,1),t=o(o.s=a[0]))}return t}var r={},s={app:0},n=[];function o(e){if(r[e])return r[e].exports;var a=r[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,o),a.l=!0,a.exports}o.m=t,o.c=r,o.d=function(t,e,a){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},o.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(o.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var r in t)o.d(a,r,function(e){return t[e]}.bind(null,r));return a},o.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],l=i.push.bind(i);i.push=e,i=i.slice();for(var c=0;c<i.length;c++)e(i[c]);var u=l;n.push([0,"chunk-vendors"]),a()})({0:function(t,e,a){t.exports=a("56d7")},"0cdb":function(t,e,a){"use strict";var r=a("4345"),s=a.n(r);s.a},"191b":function(t,e,a){"use strict";var r=a("7b57"),s=a.n(r);s.a},"1dd7":function(t,e,a){"use strict";var r=a("3164"),s=a.n(r);s.a},3164:function(t,e,a){},3450:function(t,e,a){},4345:function(t,e,a){},5333:function(t,e,a){},"56d7":function(t,e,a){"use strict";a.r(e);a("cadf"),a("551c"),a("f751"),a("097d");var r=a("2b0e"),s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{attrs:{id:"app",fluid:""}},[a("b-row",[a("b-col",{staticClass:"d-none d-md-block bg-light",attrs:{md:"3",lg:"2",id:"sidebar"}},[a("SideBar")],1),a("b-col",{attrs:{md:"9",lg:"10"}},[a("router-view",{staticStyle:{"margin-top":"1%"}})],1)],1)],1)},n=[],o=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"sidebar"},[a("b-card",{attrs:{"no-body":""}},[a("b-card-header",{staticClass:"bg-transparent"},[t._v("Projects")]),a("b-list-group",{attrs:{flush:""}},t._l(t.projects,function(e){return a("b-list-group-item",{key:e.repo,staticClass:"list-group-item"},[e.pinned?a("span",{staticClass:"oi oi-pin",attrs:{title:"pin","aria-hidden":"true"}}):t._e(),a("a",{attrs:{href:"/"+e.owner}},[t._v(t._s(e.owner))]),a("span",[t._v("/")]),a("a",{attrs:{href:"/"+e.repo}},[t._v(t._s(e.repo.replace(e.owner+"/","")))])])}),1)],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-header",[t._v("Topics")]),a("b-list-group",{attrs:{flush:""}},t._l(t.topics,function(e){return a("b-list-group-item",{key:e.type+"/"+e.repo+"/"+e.id,staticClass:"topic-item"},[e.pinned?a("span",{staticClass:"oi oi-pin",attrs:{title:"pin","aria-hidden":"true"}}):t._e(),a("a",{attrs:{href:(e.repo?"/"+e.repo:"")+"/"+e.type+"/"+e.id}},[a("span",{staticClass:"topic-prefix-brief"},[t._v(t._s(t.topicPrefixBrief(e)))]),a("span",{staticClass:"topic-prefix"},[t._v(t._s(t.topicPrefix(e)))]),a("span",[t._v(t._s(e.title))])])])}),1)],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-header",[t._v("People")]),a("b-list-group",{attrs:{flush:""}},t._l(t.people,function(e){return a("b-list-group-item",{key:e.name},[e.pinned?a("span",{staticClass:"oi oi-pin",attrs:{title:"pin","aria-hidden":"true"}}):t._e(),a("a",{attrs:{href:"/"+e.name}},[t._v(t._s(e.name))])])}),1)],1)],1)},i=[];a("4917");function l(t){var e=t.match(/[^\/]+\/(.*)/);return e?e[1]:""}var c={name:"SideBar",data:function(){return{projects:[{owner:"Cooperation",repo:"Cooperation/A"},{owner:"Alice",repo:"Alice/B"},{owner:"Bob",repo:"Bob/C"}],topics:[{type:"issues",id:11,repo:"Cooperation/A",title:"something broken.",pinned:!0},{type:"topics",id:9,title:"Some open topics",repo:""},{type:"pull",id:343,title:"Fix #87",repo:"Bob/C"}],people:[{name:"Alice"},{name:"Bob"}]}},methods:{repoName:l,topicPrefixBrief:function(t){if("topics"==t.type)return"";var e=l(t.repo),a="pull"==t.type?"PR":"#";return"["+e+" "+a+t.id+"]"},topicPrefix:function(t){if("topics"==t.type)return"";var e=t.repo,a="pull"==t.type?"PR":"#";return"["+e+" "+a+t.id+"]"}}},u=c,p=(a("0cdb"),a("2877")),d=Object(p["a"])(u,o,i,!1,null,"2fe58e2a",null),m=d.exports,b={name:"app",components:{SideBar:m}},f=b,v=(a("9062"),Object(p["a"])(f,s,n,!1,null,"0fbf8216",null)),h=v.exports,_=a("8c4f"),g=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},[a("p",[t._v("dashboard")]),a("b-card",{attrs:{title:"Message 1"}},[a("b-card-text",[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])],1),a("b-card",{attrs:{title:"Message 2"}},[a("b-card-text",[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])],1),a("b-card",{attrs:{title:"Message 3"}},[a("b-card-text",[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])],1)],1)},w=[],y={name:"DashBoard",data:function(){return{}}},C=y,x=(a("8e53"),Object(p["a"])(C,g,w,!1,null,"8c6a53ae",null)),k=x.exports,S=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"dashboard"},[a("RepoNav"),a("div",{staticStyle:{padding:"0.2rem 1rem 0.2rem 1rem"}},[t._v("descriptions")]),a("b-nav",{staticClass:"border rounded",staticStyle:{padding:"0.2rem 0"},attrs:{pills:"",fill:""}},[a("b-nav-item",[a("a",{staticClass:"nav-link",attrs:{href:"#"}},[t._v("xx commits")])]),a("b-nav-item",[a("a",{staticClass:"nav-link",attrs:{href:"#"}},[t._v("xx branches")])]),a("b-nav-item",[a("a",{staticClass:"nav-link",attrs:{href:"#"}},[t._v("xx releases")])]),a("b-nav-item",[a("a",{staticClass:"nav-link",attrs:{href:"#"}},[t._v("xx contributors")])]),a("b-nav-item",[a("a",{staticClass:"nav-link",attrs:{href:"#"}},[t._v("View lisence")])])],1),a("b-row",{staticStyle:{"white-space":"nowrap","overflow-x":"hidden"}},[a("b-col",{attrs:{cols:"2"}},[a("button",{staticClass:"btn btn-sm btn-secondary dropdown-toggle",attrs:{type:"button"}},[t._v("Branch: master")])]),a("b-col",{attrs:{cols:"2"}},[a("button",{staticClass:"d-none d-md-inline-block btn btn-sm btn-secondary",attrs:{type:"button"}},[t._v("New pull request")])]),a("b-col",{staticStyle:{overflow:"hidden"},attrs:{cols:"3",offset:"3"}},[a("b-btn-group",{staticClass:"-md-inline-flex"},[a("b-button",{attrs:{variant:"secondary",size:"sm"}},[t._v("Create new file")]),a("b-button",{attrs:{variant:"secondary",size:"sm"}},[t._v("Upload files")]),a("b-button",{attrs:{variant:"secondary",size:"sm"}},[t._v("Find file")])],1),t._v(" \n    ")],1),a("div",{staticClass:"clone"},[a("b-dropdown",{staticClass:"col-2",attrs:{variant:"success",boundary:"window",right:"",size:"sm",text:"Clone or download"}},[a("b-dropdown-item",[t._v("Clone: http...git")]),a("b-dropdown-item",[t._v("Download: http...zip")])],1)],1)],1),a("b-card",{staticClass:"filelist",attrs:{"no-body":""}},[a("b-card-header",[t._v("last commit message")]),a("b-list-group",{attrs:{flush:""}},[a("b-list-group-item",[t._v("file1")]),a("b-list-group-item",[t._v("file2")]),a("b-list-group-item",[t._v("file3")])],1)],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-header",[t._v("readme")]),a("b-card-body",[t._v("readme...")])],1)],1)},$=[],j=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"reponav"},[a("div",{staticClass:"bg-light",staticStyle:{padding:"0 1%"}},[a("h4",{staticStyle:{padding:"0.5rem 2%"}},[a("a",{attrs:{href:"/"+t.$route.params.owner}},[t._v(t._s(t.$route.params.owner))]),a("strong",[t._v("/")]),a("a",{attrs:{href:"/"+t.fullRepoName()}},[t._v(t._s(t.$route.params.repo))])]),a("b-nav",{attrs:{tabs:""}},[a("b-nav-item",{attrs:{active:"Repo"==t.$route.name,href:"/"+t.fullRepoName()}},[t._v("Code")]),a("b-nav-item",{attrs:{active:"Issue"==t.$route.name,href:"/"+t.fullRepoName()+"/issues"}},[t._v("Issues")]),a("b-nav-item",{attrs:{active:"PullRequest"==t.$route.name,href:"/"+t.fullRepoName()+"/pull"}},[t._v("Pull request")])],1)],1)])},P=[],R={name:"Profile",data:function(){return{msg:"Welcome to Your Vue.js App"}},methods:{fullRepoName:function(){return this.$route.params.owner+"/"+this.$route.params.repo}}},O=R,E=(a("76b9"),Object(p["a"])(O,j,P,!1,null,"2ed296c1",null)),q=E.exports,B={name:"Profile",data:function(){return{msg:"Welcome to Your Vue.js App"}},components:{RepoNav:q}},N=B,A=(a("f9c8"),Object(p["a"])(N,S,$,!1,null,"9d71d9d8",null)),T=A.exports,D=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{staticClass:"dashboard"},["Topic"!=t.$route.name?a("RepoNav"):t._e(),a("b-card",{attrs:{"no-body":""}},[a("b-card-body",[a("h5",{staticClass:"card-title"},[t._v("Title")]),a("p",{staticClass:"card-text"},[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])])],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-body",[a("h5",{staticClass:"card-title"},[t._v("Reply 1")]),a("p",{staticClass:"card-text"},[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])])],1),a("b-card",{attrs:{"no-body":""}},[a("b-card-body",[a("h5",{staticClass:"card-title"},[t._v("Reply 2")]),a("p",{staticClass:"card-text"},[t._v("Some quick example text to build on the card title and make up the bulk of the card's content.")])])],1)],1)},U=[],M={name:"Profile",data:function(){return{msg:"Welcome to Your Vue.js App"}},components:{RepoNav:q}},z=M,G=(a("f45f"),Object(p["a"])(z,D,U,!1,null,"4fbba046",null)),I=G.exports,V=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"login"}},[t._m(0),a("h2",{staticStyle:{"text-align":"center"}},[t._v("Sign in to Gapsule")]),t.show?a("b-form",{on:{submit:t.onSubmit,reset:t.onReset}},[a("ul",{staticClass:"main"},[a("li",{staticClass:"username"},[a("label",{attrs:{for:"username"}},[t._v("Username")]),a("b-form-input",{attrs:{id:"username",type:"text",required:"",placeholder:"Enter Username"},model:{value:t.form.username,callback:function(e){t.$set(t.form,"username",e)},expression:"form.username"}})],1),a("li",{staticClass:"password"},[a("label",{attrs:{for:"password"}},[t._v("Password")]),a("a",{staticStyle:{float:"right"},attrs:{href:"#"}},[t._v("Forget Password?")]),a("b-form-input",{attrs:{id:"password",type:"password",required:"",placeholder:"Enter password"},model:{value:t.form.password,callback:function(e){t.$set(t.form,"password",e)},expression:"form.password"}})],1),a("li",{staticClass:"operation"},[a("b-button",{staticClass:"submit",attrs:{type:"submit",variant:"primary"}},[t._v("Submit")]),a("b-button",{staticClass:"reset",attrs:{type:"reset",variant:"danger"}},[t._v("Reset")])],1)])]):t._e(),t._m(1)],1)},Y=[function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"logo"},[r("img",{attrs:{src:a("c046"),alt:"Logo"}})])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"create-account"},[a("span",[t._v("New to Gapsule?")]),a("a",{attrs:{href:"#"}},[t._v("Create an account")])])}],F=a("bc3a"),J=a.n(F),L={data:function(){return{form:{username:"",password:""},show:!0}},methods:{onSubmit:function(){J()({method:"POST",data:{username:this.form.username,password:this.form.password}}).then(function(t){200==t.status&&(window.location.href="/index")})},onReset:function(t){var e=this;t.preventDefault(),this.form.username="",this.form.password="",this.show=!1,this.$nextTick(function(){e.show=!0})}}},W=L,H=(a("1dd7"),Object(p["a"])(W,V,Y,!1,null,"0121a8d6",null)),K=H.exports,Q=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"signup"}},[a("h2",{staticStyle:{"text-align":"center"}},[t._v("Join Gapsule")]),t.show?a("b-form",{on:{submit:t.onSubmit,reset:t.onReset}},[a("ul",{staticClass:"main"},[a("li",{staticClass:"username"},[a("label",{attrs:{for:"username"}},[t._v("Username")]),a("b-form-input",{attrs:{id:"username",type:"text",required:"",placeholder:"Enter Username"},model:{value:t.form.username,callback:function(e){t.$set(t.form,"username",e)},expression:"form.username"}})],1),a("li",{staticClass:"email"},[a("label",{attrs:{for:"email"}},[t._v("Email")]),a("b-form-input",{attrs:{id:"email",type:"email",required:"",placeholder:"Enter Username"},model:{value:t.form.email,callback:function(e){t.$set(t.form,"email",e)},expression:"form.email"}})],1),a("li",{staticClass:"password"},[a("label",{attrs:{for:"password"}},[t._v("Password")]),a("b-input",{attrs:{id:"password",required:"",state:t.validation,type:"password"},model:{value:t.form.password,callback:function(e){t.$set(t.form,"password",e)},expression:"form.password"}}),a("b-form-invalid-feedback",{attrs:{state:t.validation}},[t._v("\n          Your password must be 6-18 characters long\n        ")]),a("b-form-valid-feedback",{attrs:{state:t.validation}},[t._v("\n          Looks good\n        ")])],1),a("li",{staticClass:"operation"},[a("b-button",{staticClass:"submit",attrs:{type:"submit",variant:"primary"}},[t._v("Submit")]),a("b-button",{staticClass:"reset",attrs:{type:"reset",variant:"danger"}},[t._v("Reset")])],1)])]):t._e()],1)},X=[],Z={data:function(){return{form:{username:"",password:"",email:""},show:!0}},methods:{onSubmit:function(t){t.preventDefault()},onReset:function(t){var e=this;t.preventDefault(),this.form.username="",this.form.password="",this.form.email="",this.show=!1,this.$nextTick(function(){e.show=!0})}},computed:{validation:function(){return this.form.password.length>=6&&this.form.password.length<=18}}},tt=Z,et=(a("e594"),Object(p["a"])(tt,Q,X,!1,null,"47a1fdd6",null)),at=et.exports;r["a"].use(_["a"]);var rt=new _["a"]({mode:"history",routes:[{path:"/",name:"DashBoard",component:k},{path:"/:owner/:repo",name:"Repo",component:T},{path:"/topics/:title",name:"Topic",component:I},{path:"/:owner/:repo",name:"Repo",component:T},{path:"/:owner/:repo/issues/:issueid",name:"Issue",component:I},{path:"/signin",name:"SignIn",component:K},{path:"/signup",name:"SignUp",component:at},{path:"/:owner/:repo/pull/:issueid",name:"PullRequest",component:I}]}),st=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-navbar",{staticClass:"bg-dark",attrs:{toggleable:"lg",type:"dark"}},[a("b-navbar-brand",{attrs:{href:"/"}},[t._v("Gapsule")]),a("b-navbar-toggle",{attrs:{id:"navbar-toggler",target:"navbarSupportedContent"}},[a("span",{staticClass:"navbar-toggler-icon"})]),a("b-collapse",{staticClass:"navbar-collapse",attrs:{id:"navbarSupportedContent"}},[a("b-navbar-nav",{staticClass:"mr-auto"},[a("b-nav-item",{attrs:{active:"",href:"#"}},[t._v("\n        Home\n        "),a("span",{staticClass:"sr-only"},[t._v("(current)")])]),a("b-nav-item",{attrs:{href:"#"}},[t._v("Link")]),a("b-nav-item-dropdown",{attrs:{text:"Dropdown"}},[a("b-dropdown-item",{attrs:{href:"#"}},[t._v("Action")]),a("b-dropdown-item",{attrs:{href:"#"}},[t._v("Another action")]),a("b-dropdown-divider"),a("b-dropdown-item",{attrs:{href:"#"}},[t._v("Something else here")])],1),a("b-nav-item",{attrs:{href:"#"}},[t._v("Disabled")])],1),a("b-nav-form",{staticClass:"my-2 my-lg-0",attrs:{inline:""}},[a("b-form-input",{staticClass:"form-control mr-sm-2",attrs:{type:"search",placeholder:"Search","aria-label":"Search"}}),a("b-button",{staticClass:"my-2 my-sm-0",attrs:{variant:"outline-success",type:"submit"}},[t._v("Search")])],1),t._v("\n       \n    "),a("a",{staticStyle:{color:"white"},attrs:{href:"/signin"}},[t._v("Sign in")]),t._v("\n       \n    "),a("a",{staticStyle:{color:"white"},attrs:{href:"/signup"}},[a("b-button",{staticClass:"my-2 my-sm-0",attrs:{type:"submit"}},[t._v("Sign Up")])],1)],1)],1)},nt=[],ot={name:"NavBar",mounted:function(){}},it=ot,lt=(a("191b"),Object(p["a"])(it,st,nt,!1,null,"7a4922cd",null)),ct=lt.exports,ut=a("9f7b"),pt=a.n(ut);a("f9e3"),a("2dd8");r["a"].use(pt.a),r["a"].config.productionTip=!1,r["a"].prototype.$http=J.a,new r["a"]({router:rt,render:function(t){return t(h)}}).$mount("#app"),new r["a"]({router:rt,render:function(t){return t(ct)}}).$mount("#navbar")},"575a":function(t,e,a){},"76b9":function(t,e,a){"use strict";var r=a("b6b2"),s=a.n(r);s.a},"7b57":function(t,e,a){},"8e53":function(t,e,a){"use strict";var r=a("e540"),s=a.n(r);s.a},9062:function(t,e,a){"use strict";var r=a("575a"),s=a.n(r);s.a},b629:function(t,e,a){},b6b2:function(t,e,a){},c046:function(t,e,a){t.exports=a.p+"static/img/logo.d54f0884.jpg"},e540:function(t,e,a){},e594:function(t,e,a){"use strict";var r=a("5333"),s=a.n(r);s.a},f45f:function(t,e,a){"use strict";var r=a("b629"),s=a.n(r);s.a},f9c8:function(t,e,a){"use strict";var r=a("3450"),s=a.n(r);s.a}});
//# sourceMappingURL=app.0dd92b2a.js.map