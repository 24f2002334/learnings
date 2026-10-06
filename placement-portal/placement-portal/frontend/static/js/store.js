const ppaStore = Vue.reactive({
  token: localStorage.getItem("ppa_token") || null,
  user: JSON.parse(localStorage.getItem("ppa_user") || "null"),
  profile: JSON.parse(localStorage.getItem("ppa_profile") || "null"),

  setSession(token, user, profile) {
    this.token = token;
    this.user = user;
    this.profile = profile;
    localStorage.setItem("ppa_token", token);
    localStorage.setItem("ppa_user", JSON.stringify(user));
    localStorage.setItem("ppa_profile", JSON.stringify(profile));
  },

  updateProfile(profile) {
    this.profile = profile;
    localStorage.setItem("ppa_profile", JSON.stringify(profile));
  },

  clearSession() {
    this.token = null;
    this.user = null;
    this.profile = null;
    localStorage.removeItem("ppa_token");
    localStorage.removeItem("ppa_user");
    localStorage.removeItem("ppa_profile");
  },

  isLoggedIn() {
    return !!this.token;
  },

  displayName() {
    if (!this.profile) return this.user ? this.user.email : "";
    return this.profile.name || this.user.email;
  },
});
