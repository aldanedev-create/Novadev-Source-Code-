$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$InnoScript = Join-Path $PSScriptRoot "NovaDevSetup.iss"
$Candidates = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
    "${env:LOCALAPPDATA}\Programs\Inno Setup 6\ISCC.exe"
)

$Iscc = $Candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Iscc) {
    throw "Inno Setup 6 was not found. Install it from https://jrsoftware.org/isinfo.php, then rerun this script."
}

Push-Location $RepoRoot
try {
    python scripts/build_website_downloads.py
    & $Iscc $InnoScript
    python scripts/build_website_downloads.py
    Write-Host "Built installer at: $RepoRoot\nova website\downloads\NovaDevSetup.exe"
}
finally {
    Pop-Location
}
