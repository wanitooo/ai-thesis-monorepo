const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "index-page",
        name: "index-page",
        component: () => import("pages/IndexPage.vue"),
      },
      {
        path: "tool-page",
        name: "tool-page",
        component: () => import("pages/ToolPage.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
