# NovaDev 1.0 Language Guide

NovaDev source files use the `.nova` extension. A file can contain normal
programming statements, reusable modules, or app declarations that generate
projects.

## Values

```nova
let name = "Aldane"
let title = 'NovaDev Builder'
let css = """
.featured {
    border-color: #22c55e;
}
"""
let age = 21
let active = true
let empty = nil
let tags = ["admin", "store"]
let user = { name: "Aldane", role: "owner" }
let pair = ("total", 99)
```

## Printing

```nova
print(name)
print("Hello {name}")
```

## Conditions

```nova
if age >= 18 {
    print("adult")
} elif age > 12 {
    print("teen")
} else {
    print("child")
}
```

## Loops

```nova
let count = 0
while count < 3 {
    print(count)
    count = count + 1
}

for item in tags {
    print(item)
}
```

## Functions

```nova
function add(a, b) {
    return a + b
}

print(add(2, 3))
```

## Classes

```nova
class Person {
    function init(name) {
        self.name = name
    }

    function speak() {
        return "Hello {self.name}"
    }
}

class Admin extends Person {
    function role() {
        return "admin"
    }
}
```

## Error Handling

```nova
try {
    print(missingValue)
} catch error {
    print("Handled missing value")
}
```

## App Declarations

```nova
app Store {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }

    table Product {
        id auto
        name text
        price money
    }

    page Products {
        title "Products"
        table Product {
            columns name, price
            actions view, edit, delete
        }
    }
}
```
