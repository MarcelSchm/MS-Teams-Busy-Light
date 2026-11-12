[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$versionFile = Join-Path $PSScriptRoot "version.conf"
$changelogFile = Join-Path $PSScriptRoot "changelog.md"
$tagChangelogFile = Join-Path $PSScriptRoot "changelog_currentVersion.md"
$unreleasedChangelogFile = Join-Path $PSScriptRoot "changelog_unreleased.md"
$isWindowsPlatform = [System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT
$localGitCliff = if ($isWindowsPlatform) {
    Join-Path $PSScriptRoot ".venv\Scripts\git-cliff.exe"
} else {
    Join-Path $PSScriptRoot ".venv/bin/git-cliff"
}

Push-Location $PSScriptRoot
try {
    if (Test-Path $localGitCliff) {
        $gitCliff = $localGitCliff
    } else {
        $gitCliffCommand = Get-Command git-cliff -ErrorAction SilentlyContinue
        if (-not $gitCliffCommand) {
            throw "git-cliff is required. Install the development requirements before running this script."
        }
        $gitCliff = $gitCliffCommand.Source
    }

    $versionLine = Get-Content -LiteralPath $versionFile |
        Select-String '^\s*Number\s*=\s*(\S+)\s*$' |
        Select-Object -First 1
    if (-not $versionLine -or $versionLine.Line -notmatch '^\s*Number\s*=\s*(\S+)\s*$') {
        throw "Could not read the version number from $versionFile."
    }
    $tagName = "v_$($Matches[1])"

    $localTag = git tag --list $tagName | Where-Object { $_ -eq $tagName }
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to query local Git tags."
    }
    $remoteTag = git ls-remote --tags origin "refs/tags/$tagName"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to query tags on the origin remote."
    }

    if ($localTag -or $remoteTag) {
        if ($DryRun -or $WhatIfPreference) {
            Write-Host "Tag $tagName already exists. Would update the unreleased changelog files only."
            return
        }

        & $gitCliff --unreleased --output $unreleasedChangelogFile
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to generate $unreleasedChangelogFile."
        }
        & $gitCliff --output $changelogFile
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to generate $changelogFile."
        }
        Write-Host "Tag $tagName already exists. Updated the unreleased changelog files; no commit or push was made."
        return
    }

    $branchName = git branch --show-current
    if ($LASTEXITCODE -ne 0 -or -not $branchName) {
        throw "A checked-out branch is required to create and push a release."
    }

    if ($DryRun) {
        Write-Host "Dry run: would generate changelogs, commit them, create tag $tagName, and push branch $branchName and that tag to origin."
        return
    }
    if (-not $PSCmdlet.ShouldProcess("origin", "Commit changelogs, create tag $tagName, and push")) {
        return
    }

    & $gitCliff --tag $tagName --unreleased --output $tagChangelogFile
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to generate $tagChangelogFile."
    }
    & $gitCliff --tag $tagName --output $changelogFile
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to generate $changelogFile."
    }

    git add -- $tagChangelogFile $changelogFile
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to stage generated changelogs."
    }
    git commit -m "docs: add generated changelogs for $tagName"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to commit generated changelogs."
    }
    git tag -a $tagName -F $tagChangelogFile
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create tag $tagName."
    }
    git push origin "HEAD:refs/heads/$branchName"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to push branch $branchName."
    }
    git push origin $tagName
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to push tag $tagName."
    }
} finally {
    Pop-Location
}
