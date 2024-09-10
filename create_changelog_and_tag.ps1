# This Script creates a tag based on the current version information and creates 3 changelogs:
# all changes, just the one of the latest tag and everything that is yet unreleased.
# changelog of everything that is yet unreleased is just created, if you did not increment the version.
# if you incremented it, it will automatically create a new tag with the tags changelog as well as the 
# complete changelog and push it to origin.

#  Version File name
$VERSION_FILE="version.conf"

# name of whole changelog
$CHANGELOG_FILE="changelog.md"

# name of changelog of last tag
$CHANGELOG_FILE_LAST_TAG="changelog_currentVersion.md"

# name of changelog of unreleased
$CHANGELOG_FILE_UNRELEASED="changelog_unreleased.md"

$toolName = "git-cliff" # tool for auto generating changelogs, winget name
# check if existing
$toolCheck = winget list | Select-String $toolName

if ($toolCheck) {
    # check if latest version is installed, upgrade otherwise
    winget upgrade $toolName --accept-package-agreements
} else {
    # not installed, install and restart to be able to use
    winget install  $toolName --accept-package-agreements
    Write-Output "Installed '$toolName' for you. restart of script needed, to progress further. please restart the script."
    Write-Host $_
    cmd /c 'pause'
    break
}

# Get Content of File
$VersionContent = Get-Content $VERSION_FILE

# Search for Version Name in File and store it
$specificValue = $VersionContent | Select-String 'Number = (.*)' | ForEach-Object { $_.Matches.Groups.Value }
$specificValue = $specificValue.GetValue(1)

#put string together for tag e.g. 'version_0.0.0.0'
$TagName = "v_" + $specificValue
$CurrentTags = git tag

 #Write-Output $TagName

# check if the current version in version file is already existing as a tag, otherwise create it
if ($CurrentTags -match $TagName) {
    git-cliff --unreleased  -o $CHANGELOG_FILE_UNRELEASED #writes changelog for all changes of unreleased
    git cliff -o $CHANGELOG_FILE #writes everything to changelog for all changes 
    Write-Output "The Version '$TagName' is already existing as a tag.`
     Please increment the version number in '$VERSION_FILE' and try again.`
     I wrote the current changes available for a tag to file '$CHANGELOG_FILE_UNRELEASED'."
    Write-Host $_
    cmd /c 'pause'
    break
} else {
    Write-Output "The Version '$TagName' will be created as a tag."
    # Set a tag for the unreleased changes, it doesn't have to be an existing tag and write them to changelog file
    git-cliff --tag $TagName  --unreleased -o $CHANGELOG_FILE_LAST_TAG
    git-cliff --tag $TagName -o $CHANGELOG_FILE
    git stage $CHANGELOG_FILE_LAST_TAG
    git stage $CHANGELOG_FILE
    git commit -m "docs: :memo: added changelog File with auto generated content of commit messages of latest tag."
    git tag -a "$TagName" -F "$CHANGELOG_FILE_LAST_TAG"
    git push
    git push --tag
}
