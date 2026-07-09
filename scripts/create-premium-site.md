# Project Creation

Create a new project from this starter with:

```bash
~/bin/create-premium-site my-project
```

Useful options:

```bash
~/bin/create-premium-site my-project --title "My Project"
~/bin/create-premium-site my-project --dir ~/clients
~/bin/create-premium-site my-project --no-install
~/bin/create-premium-site my-project --no-git
```

What it does:

- copies this starter without `.git`, `node_modules`, `dist`, `docs`, `.astro`, or test output
- skips `.env*` files
- updates `package.json` name
- prepends a project checklist to `README.md`
- creates `references/`, `assets/raw/`, and `public/images/`
- optionally runs `npm install`
- optionally initializes a fresh git repo and first commit

Security: it does not create GitHub repos, push, or copy secrets. Publish/deploy only after a separate secret scan and user approval.
