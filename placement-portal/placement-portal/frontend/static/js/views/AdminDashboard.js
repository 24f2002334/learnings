const AdminDashboard = {
  components: { NavBar },
  setup() {
    const stats = Vue.ref(null);
    const error = Vue.ref("");

    async function load() {
      try {
        stats.value = await api.get("/admin/dashboard");
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    return { stats, error };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <h1 class="mb-1">Overview</h1>
        <p class="ppa-muted mb-4">Institute-wide placement activity at a glance.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-if="stats" class="row g-3">
          <div class="col-6 col-md-3">
            <div class="ppa-stat">
              <div class="ppa-stat-value">{{ stats.total_students }}</div>
              <div class="ppa-stat-label">Students</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="ppa-stat">
              <div class="ppa-stat-value">{{ stats.total_companies }}</div>
              <div class="ppa-stat-label">Companies</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="ppa-stat">
              <div class="ppa-stat-value">{{ stats.total_drives }}</div>
              <div class="ppa-stat-label">Placement drives</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="ppa-stat">
              <div class="ppa-stat-value">{{ stats.total_applications }}</div>
              <div class="ppa-stat-label">Applications</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="ppa-stat" style="border-left-color:#B8860B;">
              <div class="ppa-stat-value">{{ stats.pending_companies }}</div>
              <div class="ppa-stat-label">Companies awaiting approval</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="ppa-stat" style="border-left-color:#B8860B;">
              <div class="ppa-stat-value">{{ stats.pending_drives }}</div>
              <div class="ppa-stat-label">Drives awaiting approval</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="ppa-stat" style="border-left-color:#2E7D4F;">
              <div class="ppa-stat-value">{{ stats.selected_count }}</div>
              <div class="ppa-stat-label">Students selected</div>
            </div>
          </div>
        </div>

        <div class="row g-3 mt-1">
          <div class="col-md-6">
            <router-link to="/admin/companies" class="ppa-card d-block text-decoration-none">
              <div class="ppa-section-title mb-1" style="font-size:1.05rem;">Review companies</div>
              <div class="ppa-muted ppa-small">Approve or reject pending company registrations.</div>
            </router-link>
          </div>
          <div class="col-md-6">
            <router-link to="/admin/drives" class="ppa-card d-block text-decoration-none">
              <div class="ppa-section-title mb-1" style="font-size:1.05rem;">Review drives</div>
              <div class="ppa-muted ppa-small">Approve or reject placement drives before they go live.</div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  `,
};
