const AdminDrives = {
  components: { NavBar, DataTable, StatusBadge },
  setup() {
    const drives = Vue.ref([]);
    const error = Vue.ref("");
    const statusFilter = Vue.ref("");
    const busyId = Vue.ref(null);

    const columns = [
      { key: "job_title", label: "Role" },
      { key: "company_name", label: "Company" },
      { key: "application_deadline", label: "Deadline" },
      { key: "applicant_count", label: "Applicants" },
      { key: "status", label: "Status" },
    ];

    async function load() {
      error.value = "";
      try {
        const qs = statusFilter.value ? `?status=${statusFilter.value}` : "";
        drives.value = await api.get(`/admin/drives${qs}`);
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    async function act(drive, action) {
      busyId.value = drive.id;
      try {
        await api.post(`/admin/drives/${drive.id}/${action}`);
        await load();
      } catch (e) {
        error.value = e.message;
      } finally {
        busyId.value = null;
      }
    }

    function fmtDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
    }

    return { drives, error, statusFilter, columns, busyId, load, act, fmtDate };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <h1 class="mb-1">Placement drives</h1>
        <p class="ppa-muted mb-4">Approve drives before students can see and apply to them.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div class="d-flex gap-2 mb-3">
          <select class="form-select" style="max-width:200px;" v-model="statusFilter" @change="load">
            <option value="">All statuses</option>
            <option value="Pending">Pending</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
            <option value="Closed">Closed</option>
          </select>
        </div>

        <DataTable :columns="columns" :rows="drives" empty-text="No drives match this filter.">
          <template #cell-application_deadline="{ row }">{{ fmtDate(row.application_deadline) }}</template>
          <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
          <template #actions="{ row }">
            <div class="d-flex gap-2 justify-content-end">
              <button v-if="row.status === 'Pending'" class="btn btn-sm btn-ppa-primary"
                      :disabled="busyId === row.id" @click="act(row, 'approve')">Approve</button>
              <button v-if="row.status === 'Pending'" class="btn btn-sm btn-outline-ppa"
                      :disabled="busyId === row.id" @click="act(row, 'reject')">Reject</button>
            </div>
          </template>
        </DataTable>
      </div>
    </div>
  `,
};
