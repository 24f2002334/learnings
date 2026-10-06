const Login = {
  setup() {
    const router = VueRouter.useRouter();
    const email = Vue.ref("");
    const password = Vue.ref("");
    const error = Vue.ref("");
    const loading = Vue.ref(false);

    async function submit() {
      error.value = "";
      if (!email.value || !password.value) {
        error.value = "Enter your email and password.";
        return;
      }
      loading.value = true;
      try {
        const data = await api.post("/auth/login", {
          email: email.value,
          password: password.value,
        });
        ppaStore.setSession(data.access_token, data.user, data.profile);
        const role = data.user.role;
        if (role === "admin") router.push("/admin");
        else if (role === "company") router.push("/company");
        else router.push("/student");
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    }

    return { email, password, error, loading, submit };
  },
  template: `
    <div class="ppa-auth-wrap">
      <div class="ppa-auth-card">
        <div class="ppa-auth-brand">Placement Portal</div>
        <div class="ppa-auth-sub">Sign in to continue</div>

        <div v-if="error" class="alert alert-danger py-2 ppa-small">{{ error }}</div>

        <form @submit.prevent="submit">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="email" required autofocus>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="password" required>
          </div>
          <button type="submit" class="btn btn-ppa-primary w-100" :disabled="loading">
            {{ loading ? 'Signing in…' : 'Sign in' }}
          </button>
        </form>

        <hr class="my-4">

        <div class="ppa-small ppa-muted text-center">
          New here?
          <router-link to="/register/student">Register as a student</router-link>
          or
          <router-link to="/register/company">register your company</router-link>.
        </div>
      </div>
    </div>
  `,
};
