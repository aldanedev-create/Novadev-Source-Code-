# NovaDev Documentation

NovaDev 0.5 is documented in the main `README.md`, this docs folder, and the
focused files under `novadev/docs/`.

Start with:

- [Vue Generation](vue-generation.md)
- [Backend Targets](backend-targets.md)
- [Full-Stack Projects](fullstack-projects.md)
- [Import System](import-system.md)
- [Modules](modules.md)
- [Packages](packages.md)
- [Project Structure](project-structure.md)
- [NovaDev 0.4 Background Guide](novadev-0.4-guide.md)
- [Language Guide](../novadev/docs/language-guide.md)
- [Python To NovaDev](../novadev/docs/python-to-novadev.md)
- [Python Bridge](../novadev/docs/python-bridge.md)
- [Project Generation](../novadev/docs/project-generation.md)

Useful commands:

```bash
python nova.py run examples/python_features.nova
python shell.py
python nova.py build-fullstack examples/vue_alchicken.nova
```

The older topic pages in this folder still explain the original lexer, parser,
AST, runtime, UI generator, and Flask generator ideas. For current 0.5 usage,
prefer the files listed above.
