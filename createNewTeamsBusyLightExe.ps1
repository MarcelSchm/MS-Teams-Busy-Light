[CmdletBinding()]
param(
    [switch]$AllowDefenderExclusion
)

$ErrorActionPreference = "Stop"

$repoRoot = $PSScriptRoot
$isWindowsPlatform = [System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT
$outputFolder = Join-Path $repoRoot "dist"
$venvPath = Join-Path $repoRoot ".venv"
$venvPython = if ($isWindowsPlatform) {
    Join-Path $venvPath "Scripts\python.exe"
} else {
    Join-Path $venvPath "bin/python"
}
$pyInstallerPath = if ($isWindowsPlatform) {
    Join-Path $venvPath "Scripts\pyinstaller.exe"
} else {
    Join-Path $venvPath "bin/pyinstaller"
}
$specFile = Join-Path $repoRoot "MS_Teams_Busy_Light.spec"
$versionFileScript = Join-Path $repoRoot "src\create_versionfile.py"
$requirementsFile = Join-Path $repoRoot "requirements-dev.txt"
$buildPath = $outputFolder
$necessaryFiles = @("README.md", "LICENSE", "MS_Teams_Settings.ini")

Push-Location $repoRoot
try {
    if (-not (Test-Path $venvPython)) {
        $pythonCommand = Get-Command python -ErrorAction Stop
        & $pythonCommand.Source -m venv $venvPath
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create the virtual environment."
        }
    }

    if (-not (Test-Path $requirementsFile)) {
        throw "Missing $requirementsFile. Compile it from requirements-dev.in first."
    }

    & $venvPython -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to upgrade pip."
    }
    & $venvPython -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install development requirements."
    }

    & $venvPython $versionFileScript
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to generate TeamsVersionFile.txt."
    }

    if (Test-Path $outputFolder) {
        Remove-Item -LiteralPath $outputFolder -Recurse -Force
    }

    $defenderExclusionAdded = $false
    try {
        if ($AllowDefenderExclusion -and $isWindowsPlatform) {
            if (-not (Get-Command Add-MpPreference -ErrorAction SilentlyContinue)) {
                throw "Windows Defender cmdlets are unavailable; cannot add the requested exclusion."
            }
            Write-Host "Temporarily excluding $buildPath from Windows Defender scanning."
            Add-MpPreference -ExclusionPath $buildPath
            $defenderExclusionAdded = $true
        }

        & $pyInstallerPath $specFile --noconfirm --clean --distpath $outputFolder
        if ($LASTEXITCODE -ne 0) {
            throw "PyInstaller failed with exit code $LASTEXITCODE."
        }
    } finally {
        if ($defenderExclusionAdded) {
            Remove-MpPreference -ExclusionPath $buildPath
            Write-Host "Removed the temporary Windows Defender exclusion."
        }
    }

    foreach ($file in $necessaryFiles) {
        Copy-Item -LiteralPath (Join-Path $repoRoot $file) -Destination $outputFolder -Force
    }

    $zipPath = Join-Path $outputFolder "MS_Teams_Busy_Light.zip"
    $archiveFiles = Get-ChildItem -LiteralPath $outputFolder -File |
        Where-Object { $_.FullName -ne $zipPath } |
        Select-Object -ExpandProperty FullName
    if (-not $archiveFiles) {
        throw "No build files were produced in $outputFolder."
    }
    Compress-Archive -LiteralPath $archiveFiles -DestinationPath $zipPath -Force
    Write-Host "Created $zipPath."
} finally {
    Pop-Location
}
