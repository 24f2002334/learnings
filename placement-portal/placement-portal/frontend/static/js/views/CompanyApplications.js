const CompanyApplications = {
  components: { NavBar, DataTable, StatusBadge },
  props: { driveId: [String, Number] },
  setup(props) {
    const apps = Vue.ref([]);
    const error = Vue.ref("");
    const busyId = Vue.ref(null);
    const interviewDrafts = Vue.reactive({});

    const columns = [
      { key: "student_name", label: "Student" },
      { key: "student_branch", label: "Branch" },
      { key: "student_cgpa", label: "CGPA" },
      { key: "applied_on", label: "Applied on" },
      { key: "status", label: "Status" },
    ];

    async function load() {
      error.value = "";
      try {
        apps.value = await api.get(`/company/drives/${props.driveId}/applications`);
      } catch (e) {
        error.value = e.message;
      }
    }
    Vue.onMounted(load);

    function fmtDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
    }

    async function setStatus(app, status) {
      busyId.value = app.id;
      try {
        const payload = { status };
        if (status === "Shortlisted" && interviewDrafts[app.id]) {
          payload.interview_datetime = new Date(interviewDrafts[app.id]).toISOString();
        }
        await api.put(`/company/applications/${app.id}/status`, payload);
        await load();
      } catch (e) {
        error.value = e.message;
      } finally {
        busyId.value = null;
      }
    }

    async function downloadOfferLetter(app) {
      const token = localStorage.getItem("ppa_token");
      try {
        const res = await fetch(`/api/company/applications/${app.id}/offer-letter`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.error || "Could not generate offer letter");
        }
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Offer_Letter_${(app.student_name || "candidate").replace(/\s+/g, "_")}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (e) {
        error.value = e.message;
      }
    }

    return { apps, error, columns, busyId, interviewDrafts, fmtDate, setStatus, downloadOfferLetter };
  },
  template: `
    <div class="ppa-shell">
      <NavBar />
      <div class="ppa-content">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <h1 class="mb-0">Applicants</h1>
          <router-link to="/company" class="btn btn-sm btn-outline-ppa">Back to dashboard</router-link>
        </div>
        <p class="ppa-muted mb-4">Shortlist candidates, schedule interviews, and record final outcomes.</p>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <DataTable :columns="columns" :rows="apps" empty-text="No one has applied to this drive yet.">
          <template #cell-applied_on="{ row }">{{ fmtDate(row.applied_on) }}</template>
          <template #cell-status="{ row }"><StatusBadge :status="row.status" /></template>
          <template #actions="{ row }">
            <div class="d-flex gap-2 justify-content-end align-items-center flex-wrap">
              <input v-if="row.status === 'Applied'" type="datetime-local"
                     class="form-control form-control-sm" style="width:180px;"
                     v-model="interviewDrafts[row.id]" title="Interview date/time (optional)">
              <button v-if="row.status === 'Applied'" class="btn btn-sm btn-ppa-primary"
                      :disabled="busyId === row.id" @click="setStatus(row, 'Shortlisted')">Shortlist</button>
              <button v-if="row.status === 'Shortlisted'" class="btn btn-sm btn-ppa-primary"
                      :disabled="busyId === row.id" @click="setStatus(row, 'Selected')">Select</button>
              <button v-if="['Applied','Shortlisted'].includes(row.status)" class="btn btn-sm btn-outline-ppa"
                      :disabled="busyId === row.id" @click="setStatus(row, 'Rejected')">Reject</button>
              <button v-if="row.status === 'Selected'" class="btn btn-sm btn-ppa-gold"
                      @click="downloadOfferLetter(row)">Offer letter</button>
            </div>
          </template>
        </DataTable>
      </div>
    </div>
  `,
};
