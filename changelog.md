# Changelog

All notable changes to the next MS Teams Presence Status Busy Light version are the following.

## [v_1.3.0.2] - 2024-09-11

[52c74a6](52c74a6cb23aed2d4657dc31ba543eec19fe3120)...[1b8afd2](1b8afd214ffcb133cf1af3184294fecaeb86dbb6)

### <!-- 2 -->🚜 Refactor

- Improve logging messages and variable names ([fb8ea5d](fb8ea5d158b8a33c97045f9cbdfc37e242d11cc5))


### <!-- 8 -->⚙️ Miscellaneous Tasks

- Create release.yml for github action workflow that creates a release automatically for a new tag ([74aaa27](74aaa275dc8afa373840119920221bbfefa5562f))

- Updated all pip packages to latest ([e815215](e8152159e5dcf4d18b1e2dc6fe47063b237f7faf))

- Update version number to 1.3.0.2 for first automate release workflow check and loggging info updates. ([1b8afd2](1b8afd214ffcb133cf1af3184294fecaeb86dbb6))


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