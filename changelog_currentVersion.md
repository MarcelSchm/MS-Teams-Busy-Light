# Changelog

All notable changes to the next MS Teams Presence Status Busy Light version are the following.

## [v_1.3.0.7] - 2026-11-12

[18112bd](18112bd5e01cb4cfc6fedc892778abfdaabb1dee)...[1cd356a](1cd356a69405c3081d4c84ee05eb3062c92f1e50)

### <!-- 0 -->🚀 Features

- Add support for BLINKRED status and enhance CALL case handling in LED script ([c7bb7bf](c7bb7bfc87bcb9553793aaf246d3f9b7aded43b6))

- Add new scripts for reading Teams logs, creating executables, and sending serial commands ([62e4bad](62e4badd3a517d001dcb9a5f6aecccd083720c44))

- Update requirements files to include necessary dependencies for development ([e617969](e617969a5d4b5325424b299b24fee15292ea2742))

- Add unit tests for application protocol handling and legacy configuration rejection ([aed768c](aed768ca5e27cae2f1df878c886436687b96e59f))

- Enhance changelog generation and tagging process with dry run support ([45ffe3e](45ffe3e65690e06be02382c663920e990931678f))

- Clean up .gitignore by removing obsolete build artifacts and organizing entries ([c109482](c109482296023ca15e558b7de8a6aab2dc4e93d7))

- Update README structure to enhance clarity on developer setup and add new sections for settings and Arduino setup ([549afe2](549afe20009d1a2a480de6281c5188fe094fe5ff))

- Update VSCode settings to enable pytest and configure testing environment ([2e6830d](2e6830d06faf7b1d0b9712553682c67ef2485925))

- Update release and test workflows for improved packaging and testing processes ([25874d8](25874d8b2def2317b627f9e8c81ab54ed61a288b))

- Update version number to 1.3.0.7 in version.conf ([d5b6e79](d5b6e7914f9b99f9c5a61732e2e36fdcfd027df3))

- Refactor workflows to use Ubuntu and simplify release process; update README for clarity on local builds ([1cd356a](1cd356a69405c3081d4c84ee05eb3062c92f1e50))


### <!-- 1 -->🐛 Bug Fixes

- Update file paths in MS_Teams_Busy_Light.spec to use os.path.join for better portability ([4c59c7f](4c59c7fd31dfe135fc0c62415f3f5f570eebbdd2))


### <!-- 2 -->🚜 Refactor

- Streamline log processing and command handling for Teams status updates ([89b37a5](89b37a59d0c2f8371c48f83bca86bcaf5243a686))


<!-- generated automatically by git-cliff  -->
