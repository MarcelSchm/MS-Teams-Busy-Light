$outputFolder =  ".\dist"
$pyInstallerPath = ".\.venv\Scripts\pyinstaller.exe"
$pyActivateVenv = "/.venv/Scripts/Activate.ps1"
$TeamsPy = ".\src\MS-Teams-Busy-Light.py"
$CreateVersionfile = ".\src\create_versionfile.py"
$pipRequirements = ".\requirements.txt"
$iconFile = "./images/traffic_light.ico"
$versionFile = "./TeamsVersionFile.txt"

$necessaryFiles =  ".\README.md", ".\LICENSE"

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
$temp = Join-Path (Get-Location) "\dist"
$temp = $temp -replace "`"", "'"
Add-MpPreference -ExclusionPath $temp
Start-Process -FilePath $pyInstallerPath -NoNewWindow -Wait -ArgumentList "$TeamsPy --onefile --icon=$iconFile --version-file=$versionFile --distpath $outputFolder --clean --windowed"
Remove-MpPreference -ExclusionPath $temp
Write-Output "`n`n-- Copying necessary files for execution --`n`n"
foreach ($file in $necessaryFiles)
{
    Copy-Item $file -Destination $outputFolder -Force
}
