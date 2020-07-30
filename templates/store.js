const store = new Vuex.Store({
  state: {
    // USER
    authUser: null,
    // isAuthenticated: true,
    // PROJECT
    project: null,

    site: {
      id: 1071,
      sitename: "Red Willow Pond",
    },
    observation: {
      obsType: {
        id: null,
        name: "",
      },
      kv: {},
      inOutbox: false,
      entered: false,
    },
    outbox: [1, 3, 5],
    inbox: [1, 2],
  },
  getters: {
    authUser: (state) => {
      return state.authUser;
    },
    project: (state) => {
      return state.project;
    },
    site: (state) => {
      return state.site;
    },
    observation: (state) => {
      return state.observation;
    },
  },
  mutations: {
    SET_AUTH_USER(state, authUser) {
      Vue.set(state, "authUser", authUser);
      // Vue.set(state, 'isAuthenticated', isAuthenticated)
    },
    SET_PROJECT(state, project) {
      Vue.set(state, "project", project);
    },
    SET_SITE(state, site) {
      Vue.set(state, "site", site);
    },
    SET_OBSERVATION(state, observation) {
      Vue.set(state, "observation", observation);
    },
    LOGOUT(state, authUser) {
      Vue.set(state, "authUser", null);
      Vue.set(state, "project", null);
    },
  },
  actions: {
    setAuthUser({ commit }, user) {
      commit("SET_AUTH_USER", user);
      commit("SET_PROJECT", user.default_project);
    },
    setProject({ commit }, project) {
      commit("SET_PROJECT", project);
    },
    setSite({ commit }, site) {
      commit("SET_SITE", site);
    },
    setObservation({ commit }, obj) {
      commit("SET_OBSERVATION ", obj);
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit("LOGOUT");
        // MAY NEED THIS
        // delete axios.defaults.headers.common['Authorization']
        resolve();
      });
    },
  },
});
