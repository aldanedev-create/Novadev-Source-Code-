# Vue Generation

NovaDev 0.5 can generate Vue 3 projects with Vite.

```bash
python nova.py build-vue examples/vue_alchicken.nova
```

Generated frontend structure:

```txt
frontend/
  package.json
  vite.config.js
  index.html
  src/
    main.js
    App.vue
    router/index.js
    stores/appStore.js
    services/api.js
    components/
      Sidebar.vue
      Navbar.vue
      DataTable.vue
      FormBuilder.vue
      StatCard.vue
      ChartBlock.vue
    pages/
      Dashboard.vue
      Products.vue
```

Run it:

```bash
cd generated/al-chicken/frontend
npm install
npm run dev
```

The generated Vue app uses:

- Vue 3
- Vite
- Vue Router
- Pinia
- fetch-based API calls
- custom CSS

Every NovaDev `page` becomes a Vue page component. Every `form`, `table`,
`card`, and `chart` becomes editable Vue markup that uses reusable components.
