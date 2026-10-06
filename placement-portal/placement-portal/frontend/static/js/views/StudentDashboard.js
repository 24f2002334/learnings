const StudentDashboard = {
  components: { NavBar, DataTable },
  setup() {
    const drives = Vue.ref([]);
    const error = Vue.ref("");
    const success = Vue.ref("");
    const search = Vue.ref("");
    const busyId = Vue.ref(null);
    const appliedDriveIds = Vue.ref(new Set());

    const columns = [
      { key: "job_title", label: "Role" },
      { key: "company_name", label: "Company" },
      { key: "min_cgpa", label: "Min. CGPA" },
      { key: "branch_eligible", label: "Eligible branches" },
      { key: "application_deadline", label: "Deadline" },
    ];

    async function loadAppliedIds() {
      try {
        const apps = await api.get("/student/applications");
        appliedDriveIds.value = new Set(apps.map((a) => a.drive_id));
      } catch (e) { /* ignore, non-critical */ }
    }

    async function load() {
      error.value = "";
      try {
        const qs = search.value ? `?q=${encodeURIComponent(search.value)}` : "";
        drives.value = await api.get(`/student/drives${qs}`);
      } catch (e) {
        error.value = e.message;
      }
    }

    Vue.onMounted(async () => {
      await Promise.all([load(), loadAppliedIds()]);
    });

    function fmtDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
    }

    async function apply(drive) {
      busyId.value = drive.id;
      error.value = "";
      success.value = "";
      try {
        await api.post(`/student/drives/${drive.id}/apply`);
        success.value = `Applied to ${drive.job_title} at ${drive.company_name}.`;
        appliedDriveIds.value.add(drive.id);
      } catch (e) {
        error.value = e.message;
      } finally {
        busyId.value = null;
      }
    }

    return { drives, error, success, search, columns, busyId, appliedDriveIds, load, apply, fmtDate };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <h1 class="mb-1">Open placement drives</h1>
        <p class="ppa-muted mb-4">Browse approved drives and apply if you're eligible.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <div class="d-flex gap-2 mb-3">
          <input class="form-control" style="max-width:280px;" placeholder="Search by role…"
                 v-model="search" @keyup.enter="load">
          <button class="btn btn-outline-ppa" @click="load">Search</button>
        </div>

        <DataTable :columns="columns" :rows="drives" empty-text="No approved drives are open right now — check back soon.">
          <template #cell-min_cgpa="{ row }">{{ row.min_cgpa || '—' }}</template>
          <template #cell-branch_eligible="{ row }">{{ row.branch_eligible || 'All branches' }}</template>
          <template #cell-application_deadline="{ row }">{{ fmtDate(row.application_deadline) }}</template>
          <template #actions="{ row }">
            <button v-if="!appliedDriveIds.has(row.id)" class="btn btn-sm btn-ppa-gold"
                    :disabled="busyId === row.id" @click="apply(row)">Apply</button>
            <span v-else class="ppa-badge ppa-badge-applied">Applied</span>
          </template>
        </DataTable>
      </div>
    </div>
  `,
};
