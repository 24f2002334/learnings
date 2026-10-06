const StudentProfile = {
  components: { NavBar },
  setup() {
    const form = Vue.reactive({ name: "", branch: "", cgpa: "", grad_year: "", phone: "" });
    const resumePath = Vue.ref(null);
    const error = Vue.ref("");
    const success = Vue.ref("");
    const loading = Vue.ref(false);
    const uploadFile = Vue.ref(null);

    async function load() {
      try {
        const p = await api.get("/student/profile");
        form.name = p.name || "";
        form.branch = p.branch || "";
        form.cgpa = p.cgpa != null ? p.cgpa : "";
        form.grad_year = p.grad_year || "";
        form.phone = p.phone || "";
        resumePath.value = p.resume_path;
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    async function saveProfile() {
      error.value = ""; success.value = "";
      loading.value = true;
      try {
        const p = await api.put("/student/profile", {
          ...form,
          cgpa: form.cgpa ? parseFloat(form.cgpa) : null,
          grad_year: form.grad_year ? parseInt(form.grad_year) : null,
        });
        ppaStore.updateProfile(p);
        success.value = "Profile updated.";
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    }

    function onFileChange(e) {
      uploadFile.value = e.target.files[0] || null;
    }

    async function uploadResume() {
      if (!uploadFile.value) {
        error.value = "Choose a file first.";
        return;
      }
      error.value = ""; success.value = "";
      const fd = new FormData();
      fd.append("resume", uploadFile.value);
      try {
        const res = await api.post("/student/profile/resume", fd, { isForm: true });
        resumePath.value = res.resume_path;
        success.value = "Resume uploaded.";
      } catch (e) {
        error.value = e.message;
      }
    }

    return { form, resumePath, error, success, loading, saveProfile, onFileChange, uploadResume };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content" style="max-width:600px;">
        <h1 class="mb-4">Your profile</h1>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <form @submit.prevent="saveProfile" class="ppa-card mb-4">
          <div class="mb-3">
            <label class="form-label">Full name</label>
            <input class="form-control" v-model="form.name" required>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Branch</label>
              <input class="form-control" v-model="form.branch">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Phone</label>
              <input class="form-control" v-model="form.phone" type="tel" pattern="[0-9+\-\s()]{7,15}" title="7-15 digits, may include + - ( ) and spaces">
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">CGPA</label>
              <input type="number" step="0.01" min="0" max="10" class="form-control" v-model="form.cgpa">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Graduation year</label>
              <input type="number" class="form-control" v-model="form.grad_year" min="2000" max="2100" step="1">
            </div>
          </div>
          <button type="submit" class="btn btn-ppa-primary" :disabled="loading">
            {{ loading ? 'Saving…' : 'Save changes' }}
          </button>
        </form>

        <div class="ppa-card">
          <div class="ppa-section-title" style="font-size:1.05rem;">Resume</div>
          <p class="ppa-small ppa-muted mb-2">
            {{ resumePath ? 'A resume is on file (' + resumePath + ').' : 'No resume uploaded yet.' }}
          </p>
          <input type="file" class="form-control mb-2" accept=".pdf,.doc,.docx" @change="onFileChange">
          <button class="btn btn-outline-ppa" @click="uploadResume">Upload resume</button>
        </div>
      </div>
    </div>
  `,
};
