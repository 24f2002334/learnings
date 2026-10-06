const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login, meta: { guest: true } },
  { path: "/register/student", component: RegisterStudent, meta: { guest: true } },
  { path: "/register/company", component: RegisterCompany, meta: { guest: true } },

  { path: "/admin", component: AdminDashboard, meta: { role: "admin" } },
  { path: "/admin/companies", component: AdminCompanies, meta: { role: "admin" } },
  { path: "/admin/students", component: AdminStudents, meta: { role: "admin" } },
  { path: "/admin/drives", component: AdminDrives, meta: { role: "admin" } },

  { path: "/company", component: CompanyDashboard, meta: { role: "company" } },
  { path: "/company/drives/new", component: CompanyDriveForm, meta: { role: "company" } },
  {
    path: "/company/drives/:driveId/applications",
    component: CompanyApplications,
    props: true,
    meta: { role: "company" },
  },

  { path: "/student", component: StudentDashboard, meta: { role: "student" } },
  { path: "/student/profile", component: StudentProfile, meta: { role: "student" } },
  { path: "/student/applications", component: StudentApplications, meta: { role: "student" } },
];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const loggedIn = ppaStore.isLoggedIn();
  const role = ppaStore.user && ppaStore.user.role;

  if (to.meta.guest) {
    if (loggedIn) {
      return role === "admin" ? "/admin" : role === "company" ? "/company" : "/student";
    }
    return true;
  }

  if (to.meta.role) {
    if (!loggedIn) return "/login";
    if (to.meta.role !== role) {
      return role === "admin" ? "/admin" : role === "company" ? "/company" : "/student";
    }
  }

  return true;
});

const App = {
  template: `<router-view />`,
};

const app = Vue.createApp(App);
app.use(router);
app.mount("#app");
