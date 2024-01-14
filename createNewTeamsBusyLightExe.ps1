$outputFolder =  ".\dist"
$pyInstallerPath = ".\.venv\Scripts\pyinstaller.exe"
$pyActivateVenv = "/.venv/Scripts/Activate.ps1"
$TeamsPy = ".\src\MS-Teams-Busy-Light.py"
$CreateVersionfile = ".\src\create_versionfile.py"
$pipRequirements = ".\requirements.txt"
$iconFile = "./images/traffic_light.ico"
$versionFile = "./TeamsVersionFile.txt"

$necessaryFiles =  ".\README.md", ".\LICENSE"

function New-StaticZipFile
{
  Write-Host 'Creating new .zip file'

  $Files = New-Object -TypeName 'System.Collections.ArrayList'
  $buildPath = Join-Path (Get-Location) "\dist"
  $buildPath = $buildPath -replace "`"", "'"
  $FolderItems= Get-ChildItem $buildPath -name
  $Files.Add($buildPath + '\' + $FolderItems[0])
  $Files.Add($buildPath + '\' + $FolderItems[1])
  $Files.Add($buildPath + '\' + $FolderItems[2])

  If (Test-Path -Path ($buildPath  + '\MS-Teams-Busy-Light.zip') -PathType Leaf)
  {
    Write-Host 'Deleting existing MS-Teams-Busy-Light.zip file'
    Remove-Item -Path ($buildPath  + '\MS-Teams-Busy-Light.zip')
  }

  Compress-Archive -Path $Files -DestinationPath ($buildPath  + '\MS-Teams-Busy-Light.zip')

  Write-Host 'Finished creating new MS-Teams-Busy-Light.zip file'
}


Write-Output "-- Starting to create MS Teams Busy Light executable --`n`n"
Write-Output "-- Removing old dist folder --`n`n"
Remove-Item $outputFolder -Recurse -Force -Confirm:$false
Write-Output "-- Update/Check PIP Manager --`n`n"
try {
    #generate path to venv script
    $venvsscript = Join-Path (Get-Location) $pyActivateVenv
    & $venvsscript
    python -m pip install --upgrade pip
    pip install -r $pipRequirements 
    Write-Output "`n`n"
    $userInput = Read-Host -Prompt 'Please check if there are error above. Are there Errors? (y/n)'
    if(-not ($userInput -eq 'n' -or $userInput -eq 'N')){
        throw "Error registered by user while Handling Update/Check PIP Manager. Please resolve Errors above and try again."
    }
} 
catch {
    Write-Host $_
    cmd /c 'pause'
    break
}
Write-Output "`n`n-- Creating Version File --`n`n"
python $CreateVersionfile
Write-Output "`n`n-- Starting PyInstaller --`n`n"
#trying to start pyinstaller with -windowed option results in windows antivirus error messages. therefore the folder you want to build the exe in will be setup as an exception
$buildPath = Join-Path (Get-Location) "\dist"
$buildPath = $buildPath -replace "`"", "'"
Add-MpPreference -ExclusionPath $buildPath
Start-Process -FilePath $pyInstallerPath -NoNewWindow -Wait -ArgumentList "$TeamsPy --onefile --icon=$iconFile --version-file=$versionFile --distpath $outputFolder --clean --windowed"
Remove-MpPreference -ExclusionPath $buildPath
Write-Output "`n`n-- Copying necessary files for execution --`n`n"
foreach ($file in $necessaryFiles)
{
    Copy-Item $file -Destination $outputFolder -Force
}
New-StaticZipFile


