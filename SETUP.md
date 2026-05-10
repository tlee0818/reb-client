# reb-or-kr-client — First-Run Setup

Generated package requires three one-time manual steps before CI and publishing work.

---

## 1. Enable GitHub Pages

Go to: **https://github.com/tlee0818/reb-client/settings/pages**

- Source: **GitHub Actions**

Required for the Docs workflow to deploy API reference to `https://tlee0818.github.io/reb-client/`.

---

## 2. Add PAT secret (for auto-versioning)

The semver workflow commits version bumps back to the repo. It needs a Personal Access Token with `Contents: Read+Write` on this repo.

1. Create a fine-grained PAT at **https://github.com/settings/tokens**
   - Repository access: `tlee0818/reb-client`
   - Permissions: **Contents → Read and write**
2. Add it as a repo secret named `PAT`:

```bash
gh secret set PAT --repo tlee0818/reb-client
```

---

## 3. Register PyPI Trusted Publisher

The publish workflow uses OIDC (no stored token). Register at **https://pypi.org/manage/account/publishing/**

| Field | Value |
|-------|-------|
| PyPI project name | `reb-or-kr-client` |
| Owner | `tlee0818` |
| Repository | `reb-client` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

If the package doesn't exist on PyPI yet, use **"Add a new pending publisher"**.

---

## 4. Verify

After completing the above, push any commit and confirm all workflows pass:

```bash
gh run list --repo tlee0818/reb-client --limit 5
```

Expected: CI ✓, Lint ✓, Docs ✓, Auto-version ✓
