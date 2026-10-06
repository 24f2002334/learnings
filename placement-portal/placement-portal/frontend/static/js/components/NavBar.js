const NavBar = {
  setup() {
    const router = VueRouter.useRouter();

    const links = Vue.computed(() => {
      const role = ppaStore.user && ppaStore.user.role;
      if (role === "admin") {
        return [
          { to: "/admin", label: "Dashboard" },
          { to: "/admin/companies", label: "Companies" },
          { to: "/admin/students", label: "Students" },
          { to: "/admin/drives", label: "Drives" },
        ];
      }
      if (role === "company") {
        return [
          { to: "/company", label: "Dashboard" },
        ];
      }
      if (role === "student") {
        return [
          { to: "/student", label: "Drives" },
          { to: "/student/applications", label: "My applications" },
          { to: "/student/profile", label: "Profile" },
        ];
      }
      return [];
    });

    function logout() {
      ppaStore.clearSession();
      router.push("/login");
    }

    return { links, logout, ppaStore };
  },
  template: `
    <div class="ppa-topbar">
      <div class="d-flex align-items-center gap-4">
        <span class="ppa-brand">Placement<span class="ppa-brand-accent">Portal</span></span>
        <nav class="d-none d-md-flex gap-3">
          <router-link
            v-for="l in links"
            :key="l.to"
            :to="l.to"
            class="text-decoration-none ppa-small"
            style="color:#C7CCDA;"
          >{{ l.label }}</router-link>
        </nav>
      </div>
      <div class="ppa-topbar-right">
        <span class="ppa-role-pill">{{ ppaStore.user ? ppaStore.user.role : '' }}</span>
        <span>{{ ppaStore.displayName() }}</span>
        <button class="btn btn-sm btn-outline-light" @click="logout">Log out</button>
      </div>
    </div>
  `,
};
