[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot "..\src-tauri\resources"),
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$Artifacts = @{
    FFmpeg = @{
        Url = "https://github.com/GyanD/codexffmpeg/releases/download/9.0.1/ffmpeg-9.0.1-essentials_build.zip"
        Sha256 = "fec81ae03971d9dd4be3ebe02e263bd2ec1d789483f931bdba5f5715e65da2e9"
        Size = 111253802
        FileName = "ffmpeg-9.0.1-essentials_build.zip"
    }
    Whisper = @{
        Url = "https://github.com/ggml-org/whisper.cpp/releases/download/v1.9.2/whisper-bin-x64.zip"
        Sha256 = "49dcc16de826f20bd53d44f947a1ae49dfa81f86cad67a64d80820cb192d674a"
        Size = 8194445
        FileName = "whisper-bin-x64-v1.9.2.zip"
    }
    Model = @{
        Url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
        Sha256 = "60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe"
        Size = 147951465
        FileName = "ggml-base.bin"
    }
    Font = @{
        Url = "https://raw.githubusercontent.com/google/fonts/73fc2ff52147e34a74804b500cf89ca219eac55d/ofl/notosansarabic/NotoSansArabic%5Bwdth%2Cwght%5D.ttf"
        Sha256 = "63111b5b2e074dd48cc67692e0a2726d86ee94c1c37fe8598257b7b4e87e869e"
        Size = 844676
        FileName = "NotoSansArabic.ttf"
    }
}

# yt-dlp publishes a signed SHA2-256SUMS file with every release. The version is
# pinned here and the binary is verified against the checksum file from that same
# tag, so an upstream rebuild cannot silently change what we ship.
$YtDlpVersion = "2026.07.04"

function Get-YtDlp {
    param([string]$Destination)

    $base = "https://github.com/yt-dlp/yt-dlp/releases/download/$YtDlpVersion"
    $sumsPath = Join-Path ([System.IO.Path]::GetTempPath()) "yt-dlp-$YtDlpVersion-SHA2-256SUMS"

    if (-not (Test-Path -LiteralPath $sumsPath)) {
        Invoke-WebRequest -Uri "$base/SHA2-256SUMS" -OutFile $sumsPath -MaximumRedirection 10 -UseBasicParsing
    }

    $expected = $null
    foreach ($line in Get-Content -LiteralPath $sumsPath) {
        $parts = $line -split '\s+', 2
        if ($parts.Count -eq 2 -and $parts[1].Trim() -eq "yt-dlp.exe") {
            $expected = $parts[0].Trim().ToLowerInvariant()
            break
        }
    }
    if (-not $expected) { throw "yt-dlp.exe is not listed in the $YtDlpVersion checksum file" }

    if (Test-Path -LiteralPath $Destination) {
        $current = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($current -eq $expected -and -not $Force) {
            Write-Host "Using verified cache: yt-dlp.exe"
            return
        }
        Remove-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
    }

    Write-Host "Downloading yt-dlp.exe $YtDlpVersion..."
    $lastError = $null
    foreach ($attempt in 1..3) {
        try {
            Invoke-WebRequest -Uri "$base/yt-dlp.exe" -OutFile $Destination -MaximumRedirection 10 -UseBasicParsing
            $actual = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($actual -ne $expected) {
                throw "SHA-256 verification failed for yt-dlp.exe (expected $expected, got $actual)"
            }
            return
        }
        catch {
            $lastError = $_
            Remove-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
            if ($attempt -lt 3) { Start-Sleep -Seconds (2 * $attempt) }
        }
    }
    throw $lastError
}

function Test-VerifiedFile {
    param([string]$Path, [hashtable]$Artifact)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    $file = Get-Item -LiteralPath $Path
    if ($file.Length -ne $Artifact.Size) { return $false }
    $actualHash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    return $actualHash -eq $Artifact.Sha256
}

function Get-VerifiedFile {
    param([hashtable]$Artifact, [string]$Destination)
    if (-not $Force -and (Test-VerifiedFile -Path $Destination -Artifact $Artifact)) {
        Write-Host "Using verified cache: $($Artifact.FileName)"
        return
    }

    Remove-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
    Write-Host "Downloading $($Artifact.FileName)..."
    $lastError = $null
    foreach ($attempt in 1..3) {
        try {
            Invoke-WebRequest -Uri $Artifact.Url -OutFile $Destination -MaximumRedirection 10 -UseBasicParsing
            if (-not (Test-VerifiedFile -Path $Destination -Artifact $Artifact)) {
                throw "Size or SHA-256 verification failed for $($Artifact.FileName)"
            }
            return
        }
        catch {
            $lastError = $_
            Remove-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
            if ($attempt -lt 3) { Start-Sleep -Seconds (2 * $attempt) }
        }
    }
    throw $lastError
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputDirectory)
$cacheDirectory = Join-Path ([System.IO.Path]::GetTempPath()) "easyclip-dependencies"
$extractDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("easyclip-extract-" + [Guid]::NewGuid().ToString("N"))
$binDirectory = Join-Path $resolvedOutput "bin"
$modelDirectory = Join-Path $resolvedOutput "models"
$fontDirectory = Join-Path $resolvedOutput "fonts"

New-Item -ItemType Directory -Force -Path $cacheDirectory, $extractDirectory, $binDirectory, $modelDirectory, $fontDirectory | Out-Null

try {
    $downloads = @{}
    foreach ($name in $Artifacts.Keys) {
        $artifact = $Artifacts[$name]
        $destination = Join-Path $cacheDirectory $artifact.FileName
        Get-VerifiedFile -Artifact $artifact -Destination $destination
        $downloads[$name] = $destination
    }

    $ffmpegExtract = Join-Path $extractDirectory "ffmpeg"
    $whisperExtract = Join-Path $extractDirectory "whisper"
    Expand-Archive -LiteralPath $downloads.FFmpeg -DestinationPath $ffmpegExtract -Force
    Expand-Archive -LiteralPath $downloads.Whisper -DestinationPath $whisperExtract -Force

    $ffmpeg = Get-ChildItem -Path $ffmpegExtract -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
    $ffprobe = Get-ChildItem -Path $ffmpegExtract -Recurse -Filter "ffprobe.exe" | Select-Object -First 1
    $whisperCli = Get-ChildItem -Path $whisperExtract -Recurse -Filter "whisper-cli.exe" | Select-Object -First 1
    if ($null -eq $ffmpeg -or $null -eq $ffprobe -or $null -eq $whisperCli) {
        throw "An expected executable is missing from a verified archive"
    }

    Copy-Item -LiteralPath $ffmpeg.FullName -Destination (Join-Path $binDirectory "ffmpeg.exe") -Force
    Copy-Item -LiteralPath $ffprobe.FullName -Destination (Join-Path $binDirectory "ffprobe.exe") -Force
    Copy-Item -LiteralPath $whisperCli.FullName -Destination (Join-Path $binDirectory "whisper-cli.exe") -Force

    # The official whisper.cpp Windows archive keeps its runtime DLLs beside whisper-cli.exe.
    Get-ChildItem -LiteralPath $whisperCli.DirectoryName -Filter "*.dll" -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $binDirectory $_.Name) -Force
    }

    Get-YtDlp -Destination (Join-Path $binDirectory "yt-dlp.exe")

    Copy-Item -LiteralPath $downloads.Model -Destination (Join-Path $modelDirectory "ggml-base.bin") -Force
    Copy-Item -LiteralPath $downloads.Font -Destination (Join-Path $fontDirectory "NotoSansArabic.ttf") -Force

    $manifest = [ordered]@{
        generatedAtUtc = [DateTime]::UtcNow.ToString("o")
        architecture = "x86_64-pc-windows-msvc"
        artifacts = [ordered]@{
            ffmpeg = [ordered]@{ version = "9.0.1"; sha256 = $Artifacts.FFmpeg.Sha256 }
            whisperCpp = [ordered]@{ version = "1.9.2"; sha256 = $Artifacts.Whisper.Sha256 }
            whisperModel = [ordered]@{ name = "ggml-base"; sha256 = $Artifacts.Model.Sha256 }
            captionFont = [ordered]@{ name = "Noto Sans Arabic"; sha256 = $Artifacts.Font.Sha256 }
            ytDlp = [ordered]@{ version = $YtDlpVersion }
        }
    }
    $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $resolvedOutput "runtime-manifest.json") -Encoding utf8

    Write-Host "Prepared verified EasyClip runtime resources in $resolvedOutput"
}
finally {
    Remove-Item -LiteralPath $extractDirectory -Recurse -Force -ErrorAction SilentlyContinue
}
