const DataTable = {
  props: {
    columns: Array, // [{ key, label }]
    rows: Array,
    emptyText: { type: String, default: "Nothing to show yet." },
  },
  template: `
    <div>
      <div v-if="!rows || rows.length === 0" class="ppa-empty">
        {{ emptyText }}
      </div>
      <div v-else class="ppa-table table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
              <th v-if="$slots.actions"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in rows" :key="row.id || idx">
              <td v-for="col in columns" :key="col.key">
                <slot :name="'cell-' + col.key" :row="row">{{ row[col.key] }}</slot>
              </td>
              <td v-if="$slots.actions" class="text-end">
                <slot name="actions" :row="row"></slot>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
};
