const AdminStudents = {
  components: { NavBar, DataTable, StatusBadge },
  setup() {
    const students = Vue.ref([]);
    const error = Vue.ref("");
    const search = Vue.ref("");
    const busyId = Vue.ref(null);

    const columns = [
      { key: "name", label: "Name" },
      { key: "email", label: "Email" },
      { key: "branch", label: "Branch" },
      { key: "cgpa", label: "CGPA" },
      { key: "grad_year", label: "Grad. year" },
      { key: "is_active", label: "Account" },
    ];

    async function load() {
      error.value = "";
      try {
        const qs = search.value ? `?q=${encodeURIComponent(search.value)}` : "";
        students.value = await api.get(`/admin/students${qs}`);
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    async function act(student, action) {
      busyId.value = student.id;
      try {
        await api.post(`/admin/students/${student.id}/${action}`);
        await load();
      } catch (e) {
        error.value = e.message;
      } finally {
        busyId.value = null;
      }
    }

    return { students, error, search, columns, busyId, load, act };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <h1 class="mb-1">Students</h1>
        <p class="ppa-muted mb-4">Search the student directory and manage account access.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div class="d-flex gap-2 mb-3">
          <input class="form-control" style="max-width:280px;" placeholder="Search by name or branch…"
                 v-model="search" @keyup.enter="load">
          <button class="btn btn-outline-ppa" @click="load">Search</button>
        </div>

        <DataTable :columns="columns" :rows="students" empty-text="No students match this search.">
          <template #cell-cgpa="{ row }">{{ row.cgpa != null ? row.cgpa : '—' }}</template>
          <template #cell-is_active="{ row }">
            <StatusBadge :status="row.is_active ? 'Active' : 'Inactive'" />
          </template>
          <template #actions="{ row }">
            <button v-if="row.is_active" class="btn btn-sm btn-outline-ppa"
                    :disabled="busyId === row.id" @click="act(row, 'deactivate')">Blacklist</button>
            <button v-else class="btn btn-sm btn-outline-ppa"
                    :disabled="busyId === row.id" @click="act(row, 'activate')">Reactivate</button>
          </template>
        </DataTable>
      </div>
    </div>
  `,
};
