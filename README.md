<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:92400e&height=180&section=header&text=Permission%20Audit&fontSize=38&fontColor=ffffff" width="100%" alt="Permission Audit banner"></p>
<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=19&pause=1000&color=F59E0B&center=true&vCenter=true&width=620&lines=Read-only+filesystem+permission+review;Find+world-writable+paths+before+they+surprise+you" alt="Animated tagline"></p>
<p align="center"><img src="assets/mark.svg" width="100" alt="Permission audit icon"></p>
<p align="center"><img src="https://img.shields.io/github/license/CyberLoop-dev/perm-audit?style=flat-square" alt="License"><img src="https://img.shields.io/github/languages/top/CyberLoop-dev/perm-audit?style=flat-square" alt="Language"><img src="https://img.shields.io/github/stars/CyberLoop-dev/perm-audit?style=flat-square" alt="Stars"><img src="https://img.shields.io/github/last-commit/CyberLoop-dev/perm-audit?style=flat-square" alt="Last commit"></p>

## 🧭 Overview
Permission Audit is a read-only Python command-line utility that walks a directory tree, records permission bits, and highlights paths that are world-writable or group-writable. It never changes permissions, file contents, or ownership.

## ✨ Features
- 🔍 Recursively inventory files and directories without following symlink targets.
- ⚠️ Flag world-writable and group-writable paths.
- 📋 Print a concise terminal report or machine-readable JSON.
- 🧭 Limit scan depth and optionally include entries without findings.
- 🛡️ Never chmod, delete, rename, or modify scanned paths.

## 🎬 Demo
No hosted demo is published. Run the command against a directory you own, such as the project folder.

## 🚀 Quick Start
Requires Python 3.10 or newer. No third-party packages are needed.
```bash
python main.py .
```
JSON output:
```bash
python main.py . --json
```

## 🧰 Tech Stack
- Python standard library
- `os.scandir`, `stat`, and `argparse`
- No external dependencies

## 🗂️ Folder Structure
```text
perm-audit/
├── assets/mark.svg
├── .gitignore
├── LICENSE
├── README.md
├── main.py
└── pyproject.toml
```

## 🗺️ Roadmap
- [ ] Add optional CSV output.
- [ ] Add configurable finding thresholds.
- [ ] Add a compact summary grouped by directory.

## 🤝 Contributing
Contributions are welcome. Keep the scanner read-only, do not follow symlink targets, and include platform notes for permission semantics.

## 📄 License
Released under the [MIT License](LICENSE).

<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:92400e,100:111827&height=100&section=footer" width="100%" alt="Footer wave"></p>