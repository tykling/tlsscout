# Change Log
This is the changelog for the tlsscout project. The latest version
of this file can always be found [on Github](https://github.com/tykling/tlsscout/blob/master/CHANGELOG.md)

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](http://semver.org/).


## [0.3] - 2015-04-30
### Added
- Event log showing configuration changes and engine actions
- Add a way to disable signups in the config file 
- CHANGELOG.md following the format at http://keepachangelog.com/
- Support for the ignoreName SSL Labs paramter (to ignore
  certificate name mismatches and check anyway)
- Mouseover info box on each SSL Labs grade with the IP of the 
  server and messages from the check.

### Changed
- Split settings.py into settings.py and tlsscout_settings.py,
  the latter one containing all user-configurable options.
- Formatting of site lists
- Remove unused imports from a bunch of files

### Deprecated
- Nothing

### Removed
- Nothing

### Fixed
- Hide buttons that require login from anonymous users
- Bug that prevented tag alerting from working
- last_change time for sites was not being updated
- Bug that prevented "T" and "M" grade SSL Labs results from
  being rendered.

### Security
- Nothing


## [0.2] - 2015-04-14
### Added
- Email alerting when results change
- Missing Django migrations
- Check for scheduled and running checks before scheduling 
  new checks.
- Input field for tags when creating sites

### Changed
- Nothing

### Deprecated
- Nothing

### Removed
- Django Admin disabled
- Debug output prints

### Fixed
- Lots of visual stuff, formatting and styling
- Move templatetags to the app where they belong

### Security
- Nothing


## [0.1] - 2015-03-28
- Initial release

[v0.3]: https://github.com/tykling/tlsscout/compare/v0.2...v0.3
[v0.2]: https://github.com/tykling/tlsscout/compare/v0.1...v0.2
[v0.1]: https://github.com/tykling/tlsscout/tree/v0.1
