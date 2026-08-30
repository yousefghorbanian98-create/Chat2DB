<#
.SYNOPSIS
  Muscle Paradise installer - Windows.

.DESCRIPTION
  Installs the local-first core plus the prebuilt Studio shell into
  $env:USERPROFILE\.muscle-paradise and leaves an `mp.cmd` launcher there.
  Requires Python 3.10+ and an internet connection: the bundled wheels in
  wheels\ are Linux-only, so Windows always resolves dependencies from PyPI.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\install.ps1
#>
[CmdletBinding()]
param(
  [string]$Prefix = $(if ($env:MP_PREFIX) { $env:MP_PREFIX } else { Join-Path $env:USERPROFILE ".muscle-paradise" }),
  [int]$Port = $(if ($env:MP_PORT) { [int]$env:MP_PORT } else { 8751 }),
  [switch]$WithTests
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path

function Say([string]$m) { Write-Host "==> $m" -ForegroundColor Cyan }
function Die([string]$m) { Write-Host "error: $m" -ForegroundColor Red; exit 1 }

# --- 1. find Python 3.10+ ---------------------------------------------------
$Py = $null
foreach ($cand in @("py", "python3", "python")) {
  if (Get-Command $cand -ErrorAction SilentlyContinue) {
    $ok = & $cand -c "import sys; print(1 if sys.version_info >= (3, 10) else 0)" 2>$null
    if ($ok -eq "1") { $Py = $cand; break }
  }
}
if (-not $Py) { Die "Python 3.10 or newer is required but was not found (https://python.org)." }
Say "Using Python via '$Py'"

# --- 2. lay out the prefix --------------------------------------------------
Say "Installing into $Prefix"
New-Item -ItemType Directory -Force -Path (Join-Path $Prefix "app") | Out-Null
Copy-Item -Recurse -Force (Join-Path $Here "backend") (Join-Path $Prefix "app\backend")
# Runtime assets resolved by the app as backend\..\.. (parents[3]).
Copy-Item -Recurse -Force (Join-Path $Here "assets") (Join-Path $Prefix "app\assets")
Copy-Item -Recurse -Force (Join-Path $Here "packs") (Join-Path $Prefix "app\packs")
$Studio = Join-Path $Prefix "app\studio"
if (Test-Path $Studio) { Remove-Item -Recurse -Force $Studio }
Copy-Item -Recurse -Force (Join-Path $Here "studio") $Studio
# The manifest is how `mp update` later knows what is installed and what differs.
if (Test-Path (Join-Path $Here "MANIFEST.json")) {
  Copy-Item -Force (Join-Path $Here "MANIFEST.json") (Join-Path $Prefix "app\MANIFEST.json")
}

# --- 3. virtualenv + dependencies (PyPI: bundled wheels are Linux-only) -----
$Venv = Join-Path $Prefix "venv"
if (-not (Test-Path (Join-Path $Venv "Scripts\python.exe"))) {
  Say "Creating virtualenv"
  & $Py -m venv $Venv
}
$VPy = Join-Path $Venv "Scripts\python.exe"
$Reqs = if ($WithTests) { "requirements.txt" } else { "requirements-runtime.txt" }
Say "Installing dependencies from PyPI ($Reqs)"
& $VPy -m pip install --quiet --upgrade pip
& $VPy -m pip install --quiet -r (Join-Path $Prefix "app\backend\$Reqs")

# --- 4. launcher ------------------------------------------------------------
$Launcher = Join-Path $Prefix "mp.cmd"
@"
@echo off
setlocal
set "MP_DB_PATH=%MP_DB_PATH:$($Prefix -replace '\\','\')\mp.db%"
set "MP_STATIC_DIR=$Prefix\app\studio"
set "MP_HOST=%MP_HOST:127.0.0.1%"
set "MP_PORT=$Port"
cd /d "$Prefix\app\backend"
if "%1"=="" goto start
if "%1"=="start" goto start
if "%1"=="init"  ( shift & "$VPy" -m app.bootstrap %* & goto :eof )
if "%1"=="demo"  ( shift & "$VPy" -m app.seed_demo %* & goto :eof )
if "%1"=="update" ( shift & "$VPy" -m app.updater --prefix "$Prefix" %* & goto :eof )
if "%1"=="test"  ( "$VPy" -c "import pytest" 2>nul || (echo pytest is not installed - reinstall with -WithTests & exit /b 3) & shift & "$VPy" -m pytest %* & goto :eof )
echo usage: mp [start^|init^|demo^|update^|test] & exit /b 2
:start
"$VPy" -m uvicorn app.main:create_app_from_env --factory --host %MP_HOST% --port %MP_PORT%
"@ | Set-Content -Encoding ASCII $Launcher

# --- 5. done ---------------------------------------------------------------
Say "Installed Muscle Paradise 0.19.0"
Write-Host @"

Next steps
----------
  set PATH=$Prefix;%PATH%

  set MP_OWNER_PIN=<4-6 digits>
  mp init            (creates your gym + owner account)
  mp demo            (optional demo athlete: MP-DEMO-1 / 1234)
  mp start           (serves http://127.0.0.1:$Port)
  mp test            (bundled suite; install with -WithTests to enable)

Then open http://127.0.0.1:$Port and sign in as owner, or switch to
"ورزشکار" and use MP-DEMO-1 / 1234.

Your data stays in $Prefix\mp.db - nothing leaves this machine.
"@
