# CLI Example

## About
Example of the `serialix` package usage in simple command line interface tool that can store the data in local file `settings.json`, built with help of the python built-in module `argparse` and using the `JSON_Format` configuration file.

## Commands
| Command            | Description                               |
| :----------------- | :---------------------------------------- |
| `--help`, `-h`     | show help message and exit                |
| `get` option       | get the option value                      |
| `set` option value | set the option value                      |
| `remove` option    | remove the option from configuration file |
| `clear`            | clear the configuration file              |

## Example Usage
### Set the option value
```bash
$ python cli.py set test_value 'here we go'
successfully added the new value
```
### Get the option value
```bash
$ python cli.py get test_value
here we go
```
