# CHANGELOG
## [Unreleased]
## [v1.1] - 2019-11-14
### Added:
- Added window icon
- Added a main menu using a ScreenManager
- Added basic multi-player support
- Added keyword argument support to Board constructor
- Added pip requirements file
### Changed:
- Restructured project
- Cleaned up code, added additional documentation
- Implemented Player enum instead of Board.SYMBOLS
- Game opens in full-screen by default
- Added .idea/ to .gitignore
### Fixed:
- Fixed bug that made computer not win intentionally
## [v1.02] 2019-11-08
### Added:
- Added detailed changelog
- Added spacing between buttons
### Changed:
- Increased font size
- Changed background color to white
- Starting player is now changed with every new game
## [v1.01] - 2019-11-07
### Added:
- Added .kv file
- Added reset prompt at the end of the game
- Implemented alpha-beta pruning
### Changed:
- Made code more readable
- Converted minimax() into a wrapper for play()
- Updated UI
### Removed:
- Removed unnecessary depth check
## [v1.0.0] - 2019-11-06
- Created main game with basic features
