from __future__ import annotations

"""NovaDev local package manager command.

Run:
    python novapm.py install-language --source .
    python novapm.py doctor
    python novapm.py install packages/hello-ui
"""

import argparse
import json
import sys
from pathlib import Path

from novadev.package_manager import NovaPackageManager, PackageManagerError


def manager(args) -> NovaPackageManager:
    return NovaPackageManager(home=args.home, project_root=Path.cwd())


def command_install_language(args) -> int:
    pm = manager(args)
    written = pm.install_language(args.source)
    print(f"NovaDev language installed in {pm.language_dir}")
    print(f"Launcher scripts written in {pm.bin_dir}")
    for path in written:
        print(f"  {path}")
    print_path_hint(pm)
    return 0


def command_doctor(args) -> int:
    report = manager(args).doctor()
    print(json.dumps(report, indent=2))
    if not report["languageInstalled"]:
        print("NovaDev language is not installed yet. Run: python novapm.py install-language --source .")
    return 0


def command_init_registry(args) -> int:
    path = manager(args).init_registry()
    print(f"registry initialized: {path}")
    return 0


def command_configure_registry(args) -> int:
    path = manager(args).configure_registry(args.registry)
    print(f"registry configured in {path}")
    return 0


def command_search(args) -> int:
    results = manager(args).search(args.query or "")
    if not results:
        print("no packages found")
        return 0
    for item in results:
        print(f"{item.get('name')} {item.get('version', '')} - {item.get('description', '')}")
    return 0


def command_info(args) -> int:
    print(json.dumps(manager(args).info(args.package), indent=2))
    return 0


def command_list(args) -> int:
    installed = manager(args).list_installed()
    if not installed:
        print("no packages installed")
        return 0
    for item in installed:
        print(f"{item.get('name')} {item.get('version')} - {item.get('path')}")
    return 0


def command_install(args) -> int:
    record = manager(args).install_package(args.package)
    print(f"installed {record.name} {record.version}")
    print(f"  {record.path}")
    return 0


def command_remove(args) -> int:
    manager(args).remove_package(args.package)
    print(f"removed {args.package}")
    return 0


def command_pack(args) -> int:
    target = manager(args).pack(args.package_dir, args.output)
    print(f"package written: {target}")
    return 0


def print_path_hint(pm: NovaPackageManager) -> None:
    print("")
    print("Add this folder to PATH to use nova/novapm from any terminal:")
    print(f"  {pm.bin_dir}")
    if sys.platform.startswith("win"):
        print("PowerShell example:")
        print(f'  $env:Path = "{pm.bin_dir};" + $env:Path')
    else:
        print("Shell example:")
        print(f'  export PATH="{pm.bin_dir}:$PATH"')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="novapm", description="NovaDev local package manager")
    parser.add_argument("--home", type=Path, help="NovaDev home folder, default: ~/.novadev")
    subparsers = parser.add_subparsers(dest="command")

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--home", type=Path, help=argparse.SUPPRESS)

    install_language = subparsers.add_parser("install-language", parents=[parent], help="Install NovaDev language locally")
    install_language.add_argument("--source", type=Path, default=Path("."), help="NovaDev source folder or zip")
    install_language.set_defaults(func=command_install_language)

    doctor = subparsers.add_parser("doctor", parents=[parent], help="Check local NovaDev installation")
    doctor.set_defaults(func=command_doctor)

    init_registry = subparsers.add_parser("init-registry", parents=[parent], help="Create a local package registry")
    init_registry.set_defaults(func=command_init_registry)

    configure = subparsers.add_parser("configure-registry", parents=[parent], help="Set registry path or URL")
    configure.add_argument("registry")
    configure.set_defaults(func=command_configure_registry)

    search = subparsers.add_parser("search", parents=[parent], help="Search package registry")
    search.add_argument("query", nargs="?")
    search.set_defaults(func=command_search)

    info = subparsers.add_parser("info", parents=[parent], help="Show package info")
    info.add_argument("package")
    info.set_defaults(func=command_info)

    list_parser = subparsers.add_parser("list", parents=[parent], help="List installed packages")
    list_parser.set_defaults(func=command_list)

    install = subparsers.add_parser("install", parents=[parent], help="Install a package from registry, folder, zip, or URL")
    install.add_argument("package")
    install.set_defaults(func=command_install)

    remove = subparsers.add_parser("remove", parents=[parent], help="Remove an installed package")
    remove.add_argument("package")
    remove.set_defaults(func=command_remove)

    pack = subparsers.add_parser("pack", parents=[parent], help="Pack a package folder into a zip")
    pack.add_argument("package_dir", type=Path)
    pack.add_argument("-o", "--output", type=Path)
    pack.set_defaults(func=command_pack)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except (PackageManagerError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
