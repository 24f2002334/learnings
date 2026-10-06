const RegisterStudent = {
  setup() {
    const router = VueRouter.useRouter();
    const form = Vue.reactive({
      name: "", email: "", password: "", branch: "", cgpa: "", grad_year: "", phone: "",
    });
    const error = Vue.ref("");
    const loading = Vue.ref(false);

    async function submit() {
      error.value = "";
      if (!form.name || !form.email || !form.password) {
        error.value = "Name, email and password are required.";
        return;
      }
      loading.value = true;
      try {
        await api.post("/auth/register/student", {
          ...form,
          cgpa: form.cgpa ? parseFloat(form.cgpa) : null,
          grad_year: form.grad_year ? parseInt(form.grad_year) : null,
        });
        router.push("/login");
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    }

    return { form, error, loading, submit };
  },
  template: `
    <div class="ppa-auth-wrap">
      <div class="ppa-auth-card" style="max-width:480px;">
        <div class="ppa-auth-brand">Student registration</div>
        <div class="ppa-auth-sub">Create your placement portal account</div>

        <div v-if="error" class="alert alert-danger py-2 ppa-small">{{ error }}</div>

        <form @submit.prevent="submit">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Full name</label>
              <input class="form-control" v-model="form.name" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Branch</label>
              <input class="form-control" v-model="form.branch" placeholder="e.g. CSE">
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="form.email" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="form.password" required minlength="6">
          </div>
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">CGPA</label>
              <input type="number" step="0.01" min="0" max="10" class="form-control" v-model="form.cgpa">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Grad. year</label>
              <input type="number" class="form-control" v-model="form.grad_year" placeholder="2026" min="2000" max="2100" step="1">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Phone</label>
              <input class="form-control" v-model="form.phone" type="tel" pattern="[0-9+\-\s()]{7,15}" title="7-15 digits, may include + - ( ) and spaces">
            </div>
          </div>
          <button type="submit" class="btn btn-ppa-primary w-100" :disabled="loading">
            {{ loading ? 'Creating account…' : 'Create account' }}
          </button>
        </form>

        <div class="ppa-small ppa-muted text-center mt-3">
          Already registered? <router-link to="/login">Sign in</router-link>
        </div>
      </div>
    </div>
  `,
};
