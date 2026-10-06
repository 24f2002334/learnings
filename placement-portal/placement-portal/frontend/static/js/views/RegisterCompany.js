const RegisterCompany = {
  setup() {
    const router = VueRouter.useRouter();
    const form = Vue.reactive({
      name: "", email: "", password: "", hr_contact: "", website: "", description: "",
    });
    const error = Vue.ref("");
    const loading = Vue.ref(false);
    const done = Vue.ref(false);

    async function submit() {
      error.value = "";
      if (!form.name || !form.email || !form.password) {
        error.value = "Company name, email and password are required.";
        return;
      }
      loading.value = true;
      try {
        await api.post("/auth/register/company", form);
        done.value = true;
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    }

    return { form, error, loading, done, submit };
  },
  template: `
    <div class="ppa-auth-wrap">
      <div class="ppa-auth-card" style="max-width:480px;">
        <div v-if="done">
          <div class="ppa-auth-brand">Registration submitted</div>
          <p class="ppa-muted ppa-small">
            Your company account has been created and is pending approval from the placement cell.
            You'll be able to create drives once approved.
          </p>
          <router-link to="/login" class="btn btn-ppa-primary w-100">Go to sign in</router-link>
        </div>
        <div v-else>
          <div class="ppa-auth-brand">Company registration</div>
          <div class="ppa-auth-sub">Register to start recruiting on campus</div>

          <div v-if="error" class="alert alert-danger py-2 ppa-small">{{ error }}</div>

          <form @submit.prevent="submit">
            <div class="mb-3">
              <label class="form-label">Company name</label>
              <input class="form-control" v-model="form.name" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Work email</label>
              <input type="email" class="form-control" v-model="form.email" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input type="password" class="form-control" v-model="form.password" required minlength="6">
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">HR contact</label>
                <input class="form-control" v-model="form.hr_contact">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Website</label>
                <input class="form-control" v-model="form.website" type="url" placeholder="https://example.com">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">About the company</label>
              <textarea class="form-control" rows="3" v-model="form.description"></textarea>
            </div>
            <button type="submit" class="btn btn-ppa-primary w-100" :disabled="loading">
              {{ loading ? 'Submitting…' : 'Submit for approval' }}
            </button>
          </form>

          <div class="ppa-small ppa-muted text-center mt-3">
            Already registered? <router-link to="/login">Sign in</router-link>
          </div>
        </div>
      </div>
    </div>
  `,
};
