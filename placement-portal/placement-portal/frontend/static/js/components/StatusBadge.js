const StatusBadge = {
  props: { status: String },
  template: `
    <span class="ppa-badge" :class="'ppa-badge-' + (status || '').toLowerCase()">
      {{ status }}
    </span>
  `,
};
