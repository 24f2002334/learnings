const StudentApplications = {
  components: { NavBar, DataTable, StatusBadge },
  setup() {
    const apps = Vue.ref([]);
    const error = Vue.ref("");
    const exportMessage = Vue.ref("");
    const exporting = Vue.ref(false);

    const columns = [
      { key: "company_name", label: "Company" },
      { key: "drive_title", label: "Role" },
      { key: "applied_on", label: "Applied on" },
      { key: "status", label: "Status" },
      { key: "interview_datetime", label: "Interview" },
    ];

    async function load() {
      error.value = "";
      try {
        apps.value = await api.get("/student/applications");
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    function fmtDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
    }

    async function pollExport(taskId, attempts = 0) {
      if (attempts > 20) {
        exportMessage.value = "Export is taking longer than expected — you'll receive an email once it's ready.";
        exporting.value = false;
        return;
      }
      try {
        const status = await api.get(`/student/applications/export/status/${taskId}`);
        if (status.state === "SUCCESS") {
          exportMessage.value = `Export ready (${status.result.row_count} record(s)). Check your email for the CSV attachment.`;
          exporting.value = false;
        } else if (status.state === "FAILURE") {
          exportMessage.value = "Export failed. Please try again.";
          exporting.value = false;
        } else {
          setTimeout(() => pollExport(taskId, attempts + 1), 1500);
        }
      } catch (e) {
        exportMessage.value = e.message;
        exporting.value = false;
      }
    }

    async function exportCsv() {
      exporting.value = true;
      exportMessage.value = "Export started — this runs in the background.";
      try {
        const res = await api.post("/student/applications/export", {});
        pollExport(res.task_id);
      } catch (e) {
        exportMessage.value = e.message;
        exporting.value = false;
      }
    }

    return { apps, error, exportMessage, exporting, columns, load, fmtDate, exportCsv };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-1">
          <h1 class="mb-0">My applications</h1>
          <button class="btn btn-outline-ppa" :disabled="exporting" @click="exportCsv">
            {{ exporting ? 'Exporting…' : 'Export as CSV' }}
          </button>
        </div>
        <p class="ppa-muted mb-3">Your full placement application history.</p>

        <div v-if="exportMessage" class="alert alert-info ppa-small">{{ exportMessage }}</div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <DataTable :columns="columns" :rows="apps" empty-text="You haven't applied to any drives yet.">
          <template #cell-applied_on="{ row }">{{ fmtDate(row.applied_on) }}</template>
          <template #cell-interview_datetime="{ row }">{{ fmtDate(row.interview_datetime) }}</template>
          <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
        </DataTable>
      </div>
    </div>
  `,
};
