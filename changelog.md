# Changelog

All notable changes to the next MS Teams Presence Status Busy Light version are the following.

## [v_1.3.0.4] - 2024-09-15

[bb7c180](bb7c18092fd755c4ccd334c955374a4fa6c611d8)...[9fc73a9](9fc73a9c688ec73bc3b754bfbbeeb435bbe5b0a8)

### <!-- 0 -->🚀 Features

- Add function to read from serial buffer, for more debugging options for arduino ([3c9fc14](3c9fc14d65b8428e68c098851579a18ff4a69671))


### <!-- 1 -->🐛 Bug Fixes

- Added serial flush to prevent wrong commands send to arduino sometimes ([9fc73a9](9fc73a9c688ec73bc3b754bfbbeeb435bbe5b0a8))


### <!-- 3 -->📚 Documentation

- Update version number in version.conf for new debug functionality in logs ([6c5b56e](6c5b56e12c325460451c1a0bf115e554e545d69d))

- Added changelog File with auto generated content of commit messages of latest tag. ([1d5f8ea](1d5f8ea6b4e497439599374160e045bf546a649f))


## [v_1.3.0.3] - 2024-09-15

[8981307](898130733d2cb1c0a3638b156cd2d49f9e7cbd54)...[bb7c180](bb7c18092fd755c4ccd334c955374a4fa6c611d8)

### <!-- 0 -->🚀 Features

- Update version to 1.3.0.3 and enhance debug output formatting ([dd80f61](dd80f61faeb45d14ffe4e94883d8b2f3719b80f2))


### <!-- 1 -->🐛 Bug Fixes

- Fix status color for presenceunknown in write_status_to_busy_light function ([69222db](69222db784ebbcd37de1cd21563cde6fec8d402c))


### <!-- 2 -->🚜 Refactor

- Refactor createNewTeamsBusyLightExe.ps1 script, to match (hopefully) for github actions as well. ([7cc5f76](7cc5f7699ca52f2ee0aa4956a67fdbdb16c8a39b))

- Refactor file paths in MS_Teams_Busy_Light.spec ([7cf2ee2](7cf2ee2634b26d7b6be1132baec55cbd0617e4de))

- File paths in release.yml and activate virtualenv ([a27d6d7](a27d6d7c4def02acbc55c85f61cb021909ed8fb4))

- Update release.yml to create and activate virtualenv ([2b675e0](2b675e0431cdef16db8dfb3e01614619c060e5bc))

- Update release.yml to activate virtualenv before running PowerShell script ([7bff2e8](7bff2e837ed59ad2a01ce1fa10e5ad42ea962098))

- Needed to move file to src folder ([bfdde78](bfdde784ad292459fef0516dd919d73be526fdcb))

- Update actions/checkout to v4 in release workflow and python venv paths ([fc0c7b3](fc0c7b3e3228a0b5d102069c297a9114d7ea6ae0))

- Update createNewTeamsBusyLightExeForGithubActions.py ([2c38ce7](2c38ce70d6dc6d19500bf69f890d1f2c961faca4))

- Update createNewTeamsBusyLightExeForGithubActions.py ([a7e7e50](a7e7e504a6636a6ffde07308b05887d7eeb8c87b))

- Comment out build script for release.yml (debug reasons) ([6db5719](6db5719415a1287b1f064da60914bf2c8bb00735))

- Comment out upload release assets step in release.yml ([0e3c9b9](0e3c9b9f44d65dc3b176921fa5344ad570f50816))

- Update changelog generation in release.yml ([b4a2938](b4a29383b8c1945d8851bb966c470a0a3296340c))

- Update body_path to body in release.yml ([ef76ff6](ef76ff68deec8cc9c539346579a4e5764be59252))

- Update release.yml to use updated changelog content ([3ccbd3f](3ccbd3f321673230cd1f5569d72e6231e109bd35))

- Update body_path to body in release.yml ([9241520](9241520711d2fc6b83c66a9f9fdd19763e8b375e))

- Update body_path to use direct file name ([e06c1e1](e06c1e1ac724d8105407abbb5c9e34f4f0f658e5))

- Remove code for generating changelog because it seems to duplicate generation ([eadb15b](eadb15bd649a69c1a8fa1d9bb2b974797823ab6a))


### <!-- 3 -->📚 Documentation

- Added changelog File with auto generated content of commit messages of latest tag. ([65aee2c](65aee2cb23f1600538696b262e02dd014e4ac4ca))

- Added changelog File with auto generated content of commit messages of latest tag. ([dd39224](dd39224e2d86a18d236666d8c08113dd6576c151))

- Added changelog File with auto generated content of commit messages of latest tag. ([0987571](0987571f8d9ebff2a85ca44498f1187ae60d287d))

- Added changelog File with auto generated content of commit messages of latest tag. ([7b4345b](7b4345b8325d7afeb8bd95ef8f6a04c0dbcb2379))

- Added changelog File with auto generated content of commit messages of latest tag. ([cadd70e](cadd70ebc17e7f8dcb91a1aec93fc805f73db5b1))

- Added changelog File with auto generated content of commit messages of latest tag. ([644becb](644becb3a30403242402d3fb2fd2697528392abf))

- Added changelog File with auto generated content of commit messages of latest tag. ([4a51573](4a515736ce56af3cfc980f6d7bff9e01f3c0139b))

- Added changelog File with auto generated content of commit messages of latest tag. ([4f5d09d](4f5d09d327859be8b83dcb7c8e3cd98bf5fa8f40))

- Added changelog File with auto generated content of commit messages of latest tag. ([2958e62](2958e62535dd2415a2262f8915e7f0a4c9ea0783))

- Added changelog File with auto generated content of commit messages of latest tag. ([a539e1b](a539e1b7878b5267a01a3e3deb4b8f73107c5039))

- Added changelog File with auto generated content of commit messages of latest tag. ([2b4eaea](2b4eaea076b90da457f7d6a41affbbfb7aea2f55))

- Added changelog File with auto generated content of commit messages of latest tag. ([4b47bc3](4b47bc39a1ff2f72550e5c188304f0f396817028))

- Added changelog File with auto generated content of commit messages of latest tag. ([c8bd880](c8bd88094d9d763b0f5f8cca88b80054bb88076a))

- Added changelog File with auto generated content of commit messages of latest tag. ([ca9d444](ca9d4441b127d6510f2fe980ec6ebda574c60a85))

- Added changelog File with auto generated content of commit messages of latest tag. ([9f71a16](9f71a1642f1d7fdc939b26946724823a9eb0a6aa))

- Added changelog File with auto generated content of commit messages of latest tag. ([6ba07de](6ba07de53dd160619002a986a5d48e89c54ab8c2))

- Added changelog File with auto generated content of commit messages of latest tag. ([a3470fe](a3470fe26680172aa4b55c979c6e4422a1a66140))

- Added changelog File with auto generated content of commit messages of latest tag. ([b7840aa](b7840aa04037f58c067d1993016e7570db0a1d7f))

- Added changelog File with auto generated content of commit messages of latest tag. ([bb7c180](bb7c18092fd755c4ccd334c955374a4fa6c611d8))


### <!-- 8 -->⚙️ Miscellaneous Tasks

- Update release.yml to use body_path for release notes ([5737b3e](5737b3edd1f8525de86957f9a5996e5d14dd0bc9))

- Fixed syntax error ([185e170](185e170b5e660041dc51a2a0cf6854dcd096a078))

- Fixed syntax erorrs ([3992a1c](3992a1cad0c7a188fa5ce1a45c32de571936b687))

- Fixed changelog read with git cliff ([9b356d6](9b356d6da3b762677d7e1b185343240e3a5fd9e6))

- Rewrote ps1 file to python file for github action ([842a397](842a397adfdb7c1eaeebaf20ec1369b282343be0))

- Hopefully fixed a bug with github actions and Update/Check PIP Manager function ([4587625](45876251e803df265c6fa45308973d30479bdc31))


## [v_1.3.0.2] - 2024-09-11

[52c74a6](52c74a6cb23aed2d4657dc31ba543eec19fe3120)...[8981307](898130733d2cb1c0a3638b156cd2d49f9e7cbd54)

### <!-- 1 -->🐛 Bug Fixes

- Fixed conflicting dependencies ([875c110](875c110dd06932976ef540fa6db046da05a02e39))


### <!-- 2 -->🚜 Refactor

- Improve logging messages and variable names ([fb8ea5d](fb8ea5d158b8a33c97045f9cbdfc37e242d11cc5))


### <!-- 3 -->📚 Documentation

- Added changelog File with auto generated content of commit messages of latest tag. ([55df92d](55df92d480872c70a9b1197e10c563fab30fc292))

- Added changelog File with auto generated content of commit messages of latest tag. ([20172e2](20172e248658464506f46a90a4c0ef6f18522bae))

- Added changelog File with auto generated content of commit messages of latest tag. ([61baa4b](61baa4b955ff8c997cd412f72dc0e912c6d3a884))

- Added changelog File with auto generated content of commit messages of latest tag. ([8981307](898130733d2cb1c0a3638b156cd2d49f9e7cbd54))


### <!-- 8 -->⚙️ Miscellaneous Tasks

- Create release.yml for github action workflow that creates a release automatically for a new tag ([74aaa27](74aaa275dc8afa373840119920221bbfefa5562f))

- Updated all pip packages to latest ([e815215](e8152159e5dcf4d18b1e2dc6fe47063b237f7faf))

- Update version number to 1.3.0.2 for first automate release workflow check and loggging info updates. ([1b8afd2](1b8afd214ffcb133cf1af3184294fecaeb86dbb6))

-  ci:adjusted release.yml for github action workflow for latest error messages ([c5cbda0](c5cbda0c13a711556daee4549c608f1e7b0d39fe))

-  ci:adjusted release.yml for github action workflow for latest error messages ([ef04e89](ef04e898e88f7b40b698ffbb755394dfb629e73d))

-  ci:adjusted correct path ([23e2108](23e2108730c3df696e7f287e130852d6526f170f))

-  ci:adjusted release.yml for github action workflow for latest error messages
 ([edcbd9f](edcbd9fe8e9e8a5824528c9962b7de4e7765d343))

- Add PowerShell script to create new Teams Busy Light executable ([9474178](94741788fbd1b065c6eef0918bad49c16438c36f))

- Add PowerShell script to create new Teams Busy Light executable and read changelog ([34da2db](34da2dbffd47b8ac535a44a6344546df955cb9c7))


## [v_1.3.0.1] - 2024-09-10

[0e87932](0e879325f1e3445115e4372f9dddd51f268aaea2)...[52c74a6](52c74a6cb23aed2d4657dc31ba543eec19fe3120)

### <!-- 0 -->🚀 Features

- Add git-cliff configuration file and changelog generation script ([938ef18](938ef18f289d3b392dc2de7aca78be76793066b9))

- Add git-cliff configuration file (for style of template) ([0447652](0447652516989fb7c2222fc6619e06088ff815c9))

- Add git-cliff configuration file and changelog generation script ([ea46e0a](ea46e0a1f3cb140a8f2b8418532afc23620ee6b2))


### <!-- 1 -->🐛 Bug Fixes

- Add status initialization in main loop ([886f01e](886f01ee014479ee8c1282c9cf27034a479b4141))

- Add status initialization in main loop ([028f172](028f1728dfba254361a2f75a81f7be64d9db214b))

- Add status initialization in main loop ([c227a69](c227a69c97e0d34e3e64d6dd12a6448ddc6dbcae))


### <!-- 2 -->🚜 Refactor

- Refactor create_versionfile.py and add version.conf ([39f6bda](39f6bda3483196b067ab630cd83a7247437234bd))

- Refactor create_versionfile.py and add version.conf ([bec5fb3](bec5fb35990243f60603bda7eb354aa6e5e6e93e))


### <!-- 3 -->📚 Documentation

- Updated version number to prepare for latest changes and beta version ([34b4a80](34b4a80e86f2e3149d8c40671d6dbdfcca510870))

- Added changelog File with auto generated content of commit messages of latest tag. ([3652b2b](3652b2bbf42ecf151529003686f44a250ff2595a))

- Updated version number to prepare for latest changes and beta version ([df45bf8](df45bf817ee727b535847dea33fdf0588d902e16))

- Updated version number to prepare for latest changes and beta version ([c4d2b70](c4d2b7063171ff9ed59a2389e77cff54f3dc6be1))

- Added changelog File with auto generated content of commit messages of latest tag. ([52c74a6](52c74a6cb23aed2d4657dc31ba543eec19fe3120))


## [v1.3.0-alpha] - 2024-09-09

[3d60dbc](3d60dbc71fb72171e54e7c41576118ddfa4955a5)...[0e87932](0e879325f1e3445115e4372f9dddd51f268aaea2)

### <!-- 0 -->🚀 Features

- Added new flag to config file, rebranded it to .ini and formatted a bit ([9804b72](9804b72e44579cdae27bb2884871130f67527fd2))

- Rewrote many parts of script to add functionality for new teams, as well as setable setting via .ini and logging options. ([decadf7](decadf7294dbaaf1806b674ad04cfd1545676002))


### <!-- 1 -->🐛 Bug Fixes

- Fixed a bug that the debug enabled state is always active ([144a1ee](144a1ee7de962822c43ab4ae3efca113567b1edf))

- Added explizit logging level to distinguish between debug and logging settings ([47e6b7d](47e6b7dd189d224629634b511f7e69e13c698ecd))

- Fixed that the status names in log file are different by lower casing every status, fixed some logging level errors and deleted unused imports. ([a65e9e5](a65e9e597ca5ff54db27f0e437ea857742298b05))

- Fix debug log level comparison in configure_logging function ([3ab0f44](3ab0f44283926720e8aa8c7f64085809d3b001bd))

- Fix debug log level in MS_Teams_Settings.ini ([f1961f2](f1961f2a51cb4a8887f2c3b6a81a14d5f393fec3))

- Fix logging configuration for size-based and time-based rotation ([1b0bbde](1b0bbdea5e8fdd3217bd8d03be55491b5fcab8b1))

- Fix logging configuration for size-based rotation, and update log file path ([0e87932](0e879325f1e3445115e4372f9dddd51f268aaea2))


### <!-- 3 -->📚 Documentation

- Added helpful comment for .ini ([9ed5d3f](9ed5d3ffd6930e23e807bb904963559a38c600b3))


### <!-- 5 -->🎨 Styling

- Renamed main file from '-' to '_' ([6d19985](6d19985bc34e8b6a119dc95a0c1aa9ffb5ce5aa8))

- Corrected statesettings to better values and added search string to ini file ([9b1aeae](9b1aeae9618903276e7e284f7a998ce26ed90c4d))


### <!-- 7 --> 👷 Build

- Added git ignore for logs and adjusted VS Code settings for tests ([ffa1b76](ffa1b761633e7e3dc307b128d6ba7337960d46d5))

- Moved ini file to main folder, so that it is easier for pyinstaller and .exe to access ([a35692b](a35692baa2fad336dbe07b8e8ab9d6cc4b16abf1))

- Updated version number and build script for latest changes regarding renaming and .ini file ([82e8bbc](82e8bbc20176fb41e4e87dc270885d1356d727fd))


### <!-- 8 -->⚙️ Miscellaneous Tasks

- Added newest pip packages ([b3646bf](b3646bfc777d4bc5537618200a657ce1ba412eb7))

- Added gitignore for whole build folder (due to renaming) ([f9c56fe](f9c56fef327e8396da2a5a7f0feaa23b4cb59e5d))


## [v1.2.0-alpha] - 2024-04-14

[2a6a968](2a6a9682ff2ac0dba1ed013b6b6b9368ba2839b8)...[3d60dbc](3d60dbc71fb72171e54e7c41576118ddfa4955a5)

### <!-- 2 -->🚜 Refactor

- Refactoring according to pylint
 ([25c6866](25c6866044b6d13987b72516cb9cccaf032f7b11))


## [v1.1.0] - 2024-01-14

[8504d8b](8504d8bef1237ed6f728bc7acdbe8c194701e980)...[2a6a968](2a6a9682ff2ac0dba1ed013b6b6b9368ba2839b8)

## [v1.0.1] - 2023-10-23

[d9c4412](d9c4412d479491e113c741cc04793aaff3eed750)...[8504d8b](8504d8bef1237ed6f728bc7acdbe8c194701e980)

### <!-- 1 -->🐛 Bug Fixes

- Fixed bug that it shows red when someone writes
 ([2d4bc42](2d4bc42865670f914b1e76e3d36e39590bf4dff7))


## [release] - 2023-10-22

[d8d18b9](d8d18b939156612661ad72d12c31cd2776fcf0ac)...[d9c4412](d9c4412d479491e113c741cc04793aaff3eed750)

## [test] - 2023-10-22

### <!-- 1 -->🐛 Bug Fixes

- Fixed link
 ([752b0f9](752b0f9c3e8060b99b74261fc4cde6160ed7ecc3))

- Fixed formatting ( tab instead of spaces...)
 ([109611a](109611a1687dcaa7e2ec1f3125ad009631674a9f))


<!-- generated automatically by git-cliff  -->
