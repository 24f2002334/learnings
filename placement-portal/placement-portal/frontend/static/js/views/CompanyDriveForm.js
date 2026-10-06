const CompanyDriveForm = {
  components: { NavBar },
  setup() {
    const router = VueRouter.useRouter();
    const form = Vue.reactive({
      job_title: "",
      job_description: "",
      branch_eligible: "",
      min_cgpa: "",
      grad_year_eligible: "",
      application_deadline: "",
    });
    const error = Vue.ref("");
    const loading = Vue.ref(false);
    const minDeadline = new Date(Date.now() + 60 * 1000).toISOString().slice(0, 16);

    async function submit() {
      error.value = "";
      if (!form.job_title || !form.application_deadline) {
        error.value = "Job title and application deadline are required.";
        return;
      }
      if (new Date(form.application_deadline) <= new Date()) {
        error.value = "Application deadline must be in the future.";
        return;
      }
      loading.value = true;
      try {
        await api.post("/company/drives", {
          ...form,
          min_cgpa: form.min_cgpa ? parseFloat(form.min_cgpa) : 0,
          grad_year_eligible: form.grad_year_eligible ? parseInt(form.grad_year_eligible) : null,
          application_deadline: new Date(form.application_deadline).toISOString(),
        });
        router.push("/company");
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    }

    return { form, error, loading, minDeadline, submit };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content" style="max-width:640px;">
        <h1 class="mb-1">New placement drive</h1>
        <p class="ppa-muted mb-4">This will be sent to the placement cell for approval before students can see it.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <form @submit.prevent="submit" class="ppa-card">
          <div class="mb-3">
            <label class="form-label">Job title</label>
            <input class="form-control" v-model="form.job_title" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Job description</label>
            <textarea class="form-control" rows="4" v-model="form.job_description"></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible branches</label>
              <input class="form-control" v-model="form.branch_eligible" placeholder="CSE, ECE (comma-separated, blank = all)">
            </div>
            <div class="col-md-3 mb-3">
              <label class="form-label">Min. CGPA</label>
              <input type="number" step="0.01" min="0" max="10" class="form-control" v-model="form.min_cgpa">
            </div>
            <div class="col-md-3 mb-3">
              <label class="form-label">Grad. year</label>
              <input type="number" class="form-control" v-model="form.grad_year_eligible" placeholder="blank = any" min="2000" max="2100" step="1">
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Application deadline</label>
            <input type="datetime-local" class="form-control" v-model="form.application_deadline" :min="minDeadline" required>
          </div>
          <button type="submit" class="btn btn-ppa-primary" :disabled="loading">
            {{ loading ? 'Submitting…' : 'Submit for approval' }}
          </button>
          <router-link to="/company" class="btn btn-outline-ppa ms-2">Cancel</router-link>
        </form>
      </div>
    </div>
  `,
};
