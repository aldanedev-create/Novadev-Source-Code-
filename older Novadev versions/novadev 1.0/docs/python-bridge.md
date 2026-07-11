# Python Bridge

NovaDev runs on Python 3, so it exposes useful Python-backed helpers through
`Nova.*`.

```nova
use Nova.math
use Nova.statistics
use Nova.file

print(Nova.math.sqrt(81))
print(Nova.statistics.mean([10, 20, 30]))
Nova.file.write("generated_notes/demo.txt", "Hello from NovaDev")
print(Nova.file.read("generated_notes/demo.txt"))
```

You can also use a raw Python block:

```nova
python {
    import math
    result = math.sqrt(144)
    print(result)
}
```

Python blocks are intentionally guarded. Risky imports and functions such as
`subprocess`, `ctypes`, `pickle`, `os.system`, `eval`, `exec`, and `__import__`
are blocked unless the app explicitly says:

```nova
allow unsafe_python true
```

Keep unsafe Python disabled for normal beginner projects.
