from __future__ import annotations

"""Build Vercel-hosted NovaDev download artifacts.

This script creates:

- nova website/downloads/novadev.zip
- nova website/downloads/registry.json
- nova website/downloads/checksums.json
- nova website/downloads/packages/*.zip

Run from the repository root:

    python scripts/build_website_downloads.py
"""

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEBSITE_DOWNLOADS = ROOT / "nova website" / "downloads"
WEBSITE_PACKAGES = WEBSITE_DOWNLOADS / "packages"
PACKAGE_NAMES = ["hello-ui", "auth-kit", "dashboard-kit"]

EXCLUDED_NAMES = {
    ".git",
    ".novadev",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "dist_ecommerce",
    "generated",
    "generated_backend",
    "generated_backend_django",
    "generated_backend_ecommerce",
    "generated_backend_express",
    "generated_backend_fastapi",
    "generated_docs_webshield",
    "generated_notes",
    "generated_project",
    "generated_projects",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def should_include(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    parts = relative.parts
    if any(part in EXCLUDED_NAMES or part.startswith(".tmp-") for part in parts):
        return False
    if path.suffix.lower() in {".zip", ".exe"} and parts[:2] == ("nova website", "downloads"):
        return False
    return True


def build_package_zip(name: str) -> dict[str, str]:
    source = ROOT / "packages" / name
    manifest_path = source / "nova-package.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing package manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    target = WEBSITE_PACKAGES / f"{name}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()

    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, Path(name) / path.relative_to(source))

    return {
        "name": manifest["name"],
        "version": manifest.get("version", "0.1.0"),
        "description": manifest.get("description", ""),
        "source": f"packages/{name}.zip",
        "kind": manifest.get("kind", "module"),
        "sha256": sha256(target),
    }


def build_registry() -> list[dict[str, str]]:
    packages = [build_package_zip(name) for name in PACKAGE_NAMES]
    registry = {
        "name": "novadev-official-registry",
        "version": "1.0.0",
        "description": "Website-hosted NovaDev package registry for Vercel static downloads.",
        "packages": packages,
    }
    WEBSITE_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    (WEBSITE_DOWNLOADS / "registry.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    return packages


def build_language_zip() -> Path:
    target = WEBSITE_DOWNLOADS / "novadev.zip"
    if target.exists():
        target.unlink()

    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if path.is_file() and should_include(path):
                archive.write(path, Path("novadev") / path.relative_to(ROOT))
    return target


def build_checksums(language_zip: Path) -> None:
    checksums = {"novadev.zip": sha256(language_zip)}
    for name in PACKAGE_NAMES:
        checksums[f"packages/{name}.zip"] = sha256(WEBSITE_PACKAGES / f"{name}.zip")
    setup_exe = WEBSITE_DOWNLOADS / "NovaDevSetup.exe"
    if setup_exe.exists():
        checksums["NovaDevSetup.exe"] = sha256(setup_exe)
    (WEBSITE_DOWNLOADS / "checksums.json").write_text(json.dumps(checksums, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    WEBSITE_PACKAGES.mkdir(parents=True, exist_ok=True)
    packages = build_registry()
    language_zip = build_language_zip()
    build_checksums(language_zip)

    print(f"Built {language_zip}")
    for package in packages:
        print(f"Built {package['name']} {package['version']} -> {package['source']}")
    print(f"Wrote {WEBSITE_DOWNLOADS / 'registry.json'}")
    print(f"Wrote {WEBSITE_DOWNLOADS / 'checksums.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
