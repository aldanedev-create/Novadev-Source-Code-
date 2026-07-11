# Backend Targets

NovaDev 0.5 understands these backend selectors:

```nova
backend Flask
backend FastAPI
backend Express
backend Django
```

Stack shortcuts also work:

```nova
stack VueFlask
stack VueFastAPI
stack VueNode
stack VueExpress
stack VueDjango
```

Build only the backend:

```bash
python nova.py build-backend examples/vue_alchicken.nova --target Flask
python nova.py build-backend examples/vue_security_saas.nova --target FastAPI
python nova.py build-backend examples/vue_ecommerce.nova --target Express
```

Prototype 0.5 provides the most complete backend for Flask. FastAPI, Express,
and Django are editable starter targets so the project structure is visible and
ready to extend.
