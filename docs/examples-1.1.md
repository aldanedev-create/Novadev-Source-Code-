# NovaDev 1.1 Examples

These examples use multiple `.nova` files, imports, modes, workflows, page
types, and Nova-wrapped Python modules.

```bash
python nova.py validate examples/apps/ecommerce_1_1
python nova.py validate examples/apps/construction_1_1
python nova.py validate examples/apps/crm_1_1
python nova.py validate examples/apps/school_1_1
python nova.py validate examples/apps/church_custom_1_1
python nova.py validate examples/apps/gym_custom_1_1
python nova.py validate examples/apps/security_1_1
python nova.py validate examples/apps/booking_1_1
```

Build:

```bash
python nova.py build-fullstack examples/apps/ecommerce_1_1
python nova.py build-fullstack examples/apps/construction_1_1
python nova.py build-fullstack examples/apps/church_custom_1_1
```

Inspect ProjectIR:

```bash
python nova.py ir examples/apps/ecommerce_1_1
python nova.py explain examples/apps/church_custom_1_1
```
