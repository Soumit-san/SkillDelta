// src/services/apiRoutes.js

const API = {
  auth: {
    login: "/auth/login",
    register: "/auth/register",
  },

  users: {
    me: () => "/users/me",
    update: "/users/update",
  },

  dashboard: {
    overview: (userId) => `/dashboard/user/${userId}`,
  },

  skills: {
    list: (userId) => "/skills/", // Handled by dashboard now, but keeping POST for add
    add: "/skills/",
    delete: (skillId) => `/skills/${skillId}`,
    update: (skillId) => `/skills/${skillId}`,
  },

  recommendations: {
    list: (skillId) => `/recommendations/skills/${skillId}`,
  },

  reminders: {
    list: (userId) => `/reminders/user/${userId}`,
  },

  analysis: {
    health: (skillId) => `/analysis/skills/${skillId}/health`,
    decayCurve: (skillId) => `/analysis/skills/${skillId}/decay-curve`,
  }
};

export default API;