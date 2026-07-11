# File Structure System

The architecture block lets a NovaDev app declare folders and starter files that
must exist in the generated project.

```nova
app WebShield {
    project {
        architecture {
            folder app/models
            folder app/pages
            folder app/services
            file Dockerfile
            python app/utils/FileTools.py {
                "def normalize_name(value):\n    return value.strip().lower()\n"
            }
            css app/components/dashboard.css {
                ".risk-high { color: #ef4444; }\n"
            }
        }
    }
}
```

Supported architecture entries:

- `folder path/to/folder`
- `file path/to/file`
- `python path.py { "content" }`
- `js path.js { "content" }`
- `css path.css { "content" }`
- `html path.html { "content" }`
- `sql path.sql { "content" }`

The generator creates these files before writing project docs and manifests.
