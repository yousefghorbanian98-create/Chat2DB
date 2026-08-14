# EasyClip Windows CI workflow

`easyclip-windows.yml` here is the **exact, unmodified** workflow from commit
`3f7b56c85a2d54246d9cbf571759797862831e46`.

It is parked in this directory because the Arena GitHub App token that pushed
this branch lacks the `workflows` permission, so Git refuses any push that
creates or updates files under `.github/workflows/`.

## Activating it

A user with normal repo write access must move it into place:

```bash
git checkout arena/019ffe1e-chat2db
mkdir -p .github/workflows
git mv easyclip-desktop/ci/easyclip-windows.yml .github/workflows/easyclip-windows.yml
git commit -m "Activate EasyClip Windows workflow"
git push origin arena/019ffe1e-chat2db
```

Then run it from the **Actions** tab ("EasyClip Windows Setup" -> "Run workflow"),
or with `gh workflow run easyclip-windows.yml --ref arena/019ffe1e-chat2db`.

The installer is published as the build artifact
`EasyClip-Desktop-0.2.0-Windows-x64`, containing
`EasyClip-Desktop-0.2.0-Setup.exe` and `SHA256SUMS.txt` (14-day retention).
