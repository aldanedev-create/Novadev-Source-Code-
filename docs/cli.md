# NovaDev CLI

The CLI entry point is `nova.py`.

```bash
python nova.py new my_app --frontend Vue --backend Flask --database SQLite
python nova.py run examples/scripts/math_tool.nova
python nova.py shell
python nova.py tokens examples/apps/webshield
python nova.py ast examples/apps/webshield --json
python nova.py lint examples/apps/webshield
python nova.py format examples/apps/webshield --check
python nova.py docs examples/apps/webshield
python nova.py build-ui examples/apps/webshield
python nova.py build-vue examples/apps/webshield
python nova.py build-backend examples/apps/webshield --target Flask
python nova.py build-fullstack examples/apps/webshield
python nova.py build examples/apps/webshield
python nova.py dev examples/apps/webshield
python nova.py clean generated/web-shield
python nova.py install AuthKit
python nova.py update AuthKit
python nova.py remove AuthKit
python nova.py deploy examples/apps/webshield
```

The shell supports the same project actions as dot commands:

```txt
nova> .run examples/scripts/math_tool.nova
nova> .tokens examples/apps/webshield
nova> .ast examples/apps/webshield --json
nova> .build-fullstack examples/apps/webshield
nova> .lint examples/apps/webshield
nova> .docs examples/apps/webshield
nova> .exit
```
