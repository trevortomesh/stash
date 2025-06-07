# Stash

[![Build Status](https://github.com/trevortomesh/stash/workflows/CI/badge.svg)](https://github.com/trevortomesh/stash/actions)
[![PyPI version](https://badge.fury.io/py/stash.svg)](https://badge.fury.io/py/stash)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Stash is a powerful file organization tool that helps you sort, archive, and manage your files efficiently.

## Features

- Organize files by type, date, or custom rules
- Support for archiving and backup
- Easy to use CLI interface
- Extensible with plugins

## Installation

```bash
pip install stash
```

## Troubleshooting

If you encounter issues, try the following:

- Ensure Python 3.6+ is installed
- Check your PATH environment variable includes Python scripts
- Use `stash --help` to review command options
- Report bugs on GitHub Issues

## Usage

Basic usage example:

```bash
stash sort /path/to/your/files
```

For more commands and options, use:

```bash
stash --help
```

## Configuration

Stash can be configured via a config file located at `~/.stash/config.yaml`. Example configuration:

```yaml
sort_rules:
  - extension: .txt
    destination: TextFiles/
  - extension: .jpg
    destination: Images/
```

## Tips

- Use `stash preview` to see what changes will be made without applying them.
- Combine with DeepStash for cold storage management.

## Uninstallation

To uninstall Stash:

```bash
pip uninstall stash
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, open an issue on GitHub or contact the maintainer.

## Related Projects

- **DeepStash** – A sister project to Stash that provides advanced long-term archival and external drive backup for deeply cold files.  
  [https://github.com/trevortomesh/deep-stash](https://github.com/trevortomesh/deep-stash)

  ### 🧊 Suggested Use:
  You can find and install DeepStash here: https://github.com/trevortomesh/deep-stash

  DeepStash is designed to work alongside Stash — but it also stands strong on its own. Use it to offload files and folders to a long-term archive (such as an external drive) while keeping their original location and context intact via `.ds` metadata files.

  It safely stashes your items elsewhere, leaving behind smart placeholders you can use to restore them at any time. Perfect for cleaning up your workspace without breaking your mental map of where everything lives.

  To install:
  ```bash
  git clone https://github.com/trevortomesh/deep-stash.git
  cd deep-stash
  pip install .
  ```

  To use:

  1. Set the stash location:
     ```bash
     ds --init
     ```

  2. Stash an item:
     ```bash
     ds FinalPaper.pdf
     ```

  3. Restore an item:
     ```bash
     ds FinalPaper.pdf.ds
     ```

  4. View help and advanced options:
     ```bash
     ds --help
     ```

  DeepStash integrates beautifully with Stash to offload rarely used files after sorting — but it's equally effective on its own when you just need to move things without losing your structure.
