# Check for PowerShell version 6 or higher
if ($PSVersionTable.PSVersion.Major -lt 6) {
  throw "This script requires PowerShell 6.0 or higher. Please update your PowerShell version."
}

$outputFolder =  Join-Path (Get-Location) "dist"
$pyInstallerPath = if ($IsWindows) { Join-Path (Get-Location) ".\.venv\Scripts\pyinstaller.exe" } else { Join-Path (Get-Location) ".venv/bin/pyinstaller" }
$pyActivateVenv = if ($IsWindows) { Join-Path (Get-Location) ".\.venv\Scripts\Activate.ps1" } else { Join-Path (Get-Location) ".venv/bin/activate" }
$TeamsPy = Join-Path (Get-Location) "src/MS_Teams_Busy_Light.py"
$CreateVersionfile = Join-Path (Get-Location) "src/create_versionfile.py"
$pipRequirements = Join-Path (Get-Location) "requirements.txt"
$iconFile = Join-Path (Get-Location) "images/traffic_light.ico"
$versionFile = Join-Path (Get-Location) "TeamsVersionFile.txt"

$necessaryFiles = @('README.md', 'LICENSE', 'MS_Teams_Settings.ini')

function New-StaticZipFile {
    Write-Host 'Creating new .zip file'

    $Files = New-Object -TypeName 'System.Collections.ArrayList'
    $buildPath = Join-Path (Get-Location) "dist"
    $FolderItems = Get-ChildItem $buildPath -name
    foreach ($item in $FolderItems) {
        $Files.Add((Join-Path $buildPath $item))
    }

    $zipPath = Join-Path $buildPath "MS_Teams_Busy_Light.zip"
    If (Test-Path -Path $zipPath -PathType Leaf) {
        Write-Host 'Deleting existing MS_Teams_Busy_Light.zip file'
        Remove-Item -Path $zipPath
    }

    Compress-Archive -Path $Files -DestinationPath $zipPath

    Write-Host 'Finished creating new MS_Teams_Busy_Light.zip file'
}

Write-Output "-- Starting to create MS Teams Busy Light 
 --`n`n"
Write-Output "-- Removing old dist folder --`n`n"
if (Test-Path $outputFolder) {
    Remove-Item $outputFolder -Recurse -Force -Confirm:$false
}
Write-Output "-- Update/Check PIP Manager --`n`n"
try {
    # Generate path to venv script
    $venvScript = $pyActivateVenv
    if ($IsWindows) {
        & $venvScript
    } else {
        . $venvScript
    }
    python -m pip install --upgrade pip
    pip install -r $pipRequirements 
    Write-Output "`n`n"
    $errorCheck = $null
    try {
      $errorCheck = & python -c "import sys; sys.exit(1) if any('ERROR' in line.upper() for line in sys.stderr) else sys.exit(0)"
    } catch {
      $errorCheck = $_.Exception.Message
    }
    if ($errorCheck) {
      throw "Error occurred while handling Update/Check PIP Manager. Please resolve errors above and try again."
    }
} 
catch {
    Write-Host $_
    if ($IsWindows) {
        cmd /c 'pause'
    }
    break
}
Write-Output "`n`n-- Creating Version File --`n`n"
python $CreateVersionfile
Write-Output "`n`n-- Starting PyInstaller --`n`n"
# Trying to start pyinstaller with -windowed option results in windows antivirus error messages. Therefore the folder you want to build the exe in will be setup as an exception
$buildPath = Join-Path (Get-Location) "dist"
if ($IsWindows) {
    Add-MpPreference -ExclusionPath $buildPath
}
Start-Process -FilePath $pyInstallerPath -NoNewWindow -Wait -ArgumentList "$TeamsPy --onefile --icon=$iconFile --version-file=$versionFile --distpath $outputFolder --clean --windowed"
if ($IsWindows) {
    Remove-MpPreference -ExclusionPath $buildPath
}
Write-Output "`n`n-- Copying necessary files for execution --`n`n"
foreach ($file in $necessaryFiles) {
    Copy-Item $file -Destination $outputFolder -Force
}
New-StaticZipFile