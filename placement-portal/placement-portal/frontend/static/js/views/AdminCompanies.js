const AdminCompanies = {
  components: { NavBar, DataTable, StatusBadge },
  setup() {
    const companies = Vue.ref([]);
    const error = Vue.ref("");
    const search = Vue.ref("");
    const statusFilter = Vue.ref("");
    const busyId = Vue.ref(null);

    const columns = [
      { key: "name", label: "Company" },
      { key: "hr_contact", label: "HR contact" },
      { key: "email", label: "Email" },
      { key: "approval_status", label: "Approval" },
      { key: "is_active", label: "Account" },
    ];

    async function load() {
      error.value = "";
      try {
        const params = new URLSearchParams();
        if (search.value) params.set("q", search.value);
        if (statusFilter.value) params.set("status", statusFilter.value);
        const qs = params.toString() ? `?${params.toString()}` : "";
        companies.value = await api.get(`/admin/companies${qs}`);
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    async function act(company, action) {
      busyId.value = company.id;
      try {
        await api.post(`/admin/companies/${company.id}/${action}`);
        await load();
      } catch (e) {
        error.value = e.message;
      } finally {
        busyId.value = null;
      }
    }

    return { companies, error, search, statusFilter, columns, busyId, load, act };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <h1 class="mb-1">Companies</h1>
        <p class="ppa-muted mb-4">Review registrations, approve trusted recruiters, and manage access.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div class="d-flex gap-2 mb-3 flex-wrap">
          <input class="form-control" style="max-width:280px;" placeholder="Search by name…"
                 v-model="search" @keyup.enter="load">
          <select class="form-select" style="max-width:180px;" v-model="statusFilter" @change="load">
            <option value="">All statuses</option>
            <option value="Pending">Pending</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
          </select>
          <button class="btn btn-outline-ppa" @click="load">Search</button>
        </div>

        <DataTable :columns="columns" :rows="companies" empty-text="No companies match this filter.">
          <template #cell-approval_status="{ row }">
            <StatusBadge :status="row.approval_status" />
          </template>
          <template #cell-is_active="{ row }">
            <StatusBadge :status="row.is_active ? 'Active' : 'Inactive'" />
          </template>
          <template #actions="{ row }">
            <div class="d-flex gap-2 justify-content-end">
              <button v-if="row.approval_status === 'Pending'" class="btn btn-sm btn-ppa-primary"
                      :disabled="busyId === row.id" @click="act(row, 'approve')">Approve</button>
              <button v-if="row.approval_status === 'Pending'" class="btn btn-sm btn-outline-ppa"
                      :disabled="busyId === row.id" @click="act(row, 'reject')">Reject</button>
              <button v-if="row.is_active" class="btn btn-sm btn-outline-ppa"
                      :disabled="busyId === row.id" @click="act(row, 'deactivate')">Blacklist</button>
              <button v-else class="btn btn-sm btn-outline-ppa"
                      :disabled="busyId === row.id" @click="act(row, 'activate')">Reactivate</button>
            </div>
          </template>
        </DataTable>
      </div>
    </div>
  `,
};
