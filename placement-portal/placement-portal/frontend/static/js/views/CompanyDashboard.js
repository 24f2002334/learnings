const CompanyDashboard = {
  components: { NavBar, DataTable, StatusBadge },
  setup() {
    const company = Vue.ref(null);
    const drives = Vue.ref([]);
    const error = Vue.ref("");

    const columns = [
      { key: "job_title", label: "Role" },
      { key: "application_deadline", label: "Deadline" },
      { key: "applicant_count", label: "Applicants" },
      { key: "status", label: "Status" },
    ];

    async function load() {
      error.value = "";
      try {
        const data = await api.get("/company/dashboard");
        company.value = data.company;
        drives.value = data.drives;
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    function fmtDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
    }

    async function closeDrive(drive) {
      try {
        await api.post(`/company/drives/${drive.id}/close`);
        await load();
      } catch (e) {
        error.value = e.message;
      }
    }

    return { company, drives, error, columns, fmtDate, closeDrive };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <div class="d-flex justify-content-between align-items-start flex-wrap gap-2 mb-1">
          <h1 class="mb-0">{{ company ? company.name : 'Dashboard' }}</h1>
          <router-link to="/company/drives/new" class="btn btn-ppa-gold"
                       v-if="company && company.approval_status === 'Approved'">
            + New drive
          </router-link>
        </div>

        <div v-if="company" class="mb-4">
          <StatusBadge :status="company.approval_status" />
          <span v-if="company.approval_status !== 'Approved'" class="ppa-small ppa-muted ms-2">
            You can create drives once the placement cell approves your company.
          </span>
        </div>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div class="ppa-section-title">Your placement drives</div>
        <DataTable :columns="columns" :rows="drives" empty-text="You haven't created any drives yet.">
          <template #cell-application_deadline="{ row }">{{ fmtDate(row.application_deadline) }}</template>
          <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
          <template #actions="{ row }">
            <div class="d-flex gap-2 justify-content-end">
              <router-link :to="'/company/drives/' + row.id + '/applications'"
                           class="btn btn-sm btn-outline-ppa">Applications</router-link>
              <button v-if="row.status === 'Approved'" class="btn btn-sm btn-outline-ppa"
                      @click="closeDrive(row)">Close</button>
            </div>
          </template>
        </DataTable>
      </div>
    </div>
  `,
};
