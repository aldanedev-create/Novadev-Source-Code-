# Project Structure

A NovaDev folder project usually looks like this:

```txt
my_app/
  Nova.toml
  app.nova
  database/
    Product.nova
  pages/
    Dashboard.nova
```

`Nova.toml` example:

```toml
name = "MyApp"
version = "1.0"
entry = "app.nova"
frontend = "Vue"
backend = "Flask"
database = "SQLite"
```

Create a starter:

```bash
python nova.py new my_app --frontend Vue --backend Flask --database SQLite
```

Build it:

```bash
python nova.py build-fullstack my_app
```
