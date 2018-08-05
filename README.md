# Python Script: QuickConfigTemplates

## Created By: Benjamin P. Trachtenberg

### Contact Information:  e_ben_75-python@yahoo.com
### If you have any questions e-mail me

### LinkedIn: [Ben Trachtenberg](https://www.linkedin.com/in/ben-trachtenberg-3a78496)
### PyPi: [My PyPi](https://pypi.org/user/btr1975/)
### Docker Hub: [My Docker Hub](https://hub.docker.com/r/btr1975)
### Ansible Galaxy: [My Ansible Galaxy](https://galaxy.ansible.com/btr1975/)

### About

This script is for simple config templates, to make life easier on admins/engineers

### Reference Information
* [License](https://github.com/btr1975/QuickConfigTemplates/blob/master/LICENSE)
* [Directions](https://github.com/btr1975/QuickConfigTemplates/wiki)
* [YAML Format](http://yaml.org/)
* [Jinja2 Template Language](http://jinja.pocoo.org)
* [Example Configs](https://github.com/btr1975/QuickConfigTemplates/tree/master/Docs/Examples)

### Version Information
* [1.0.3.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.3.prod)
* [1.0.4.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.4.prod)
* [1.0.5.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.5.prod)
* [1.0.7.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.7.prod)
* [1.0.8.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.8.prod)
* [1.0.9.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.9.prod)
* [1.0.10.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.10.prod)
* [1.0.11.prod](https://github.com/btr1975/QuickConfigTemplates/wiki/Version-1.0.11.prod)

### Requirements
* [See Pipfile](https://github.com/btr1975/QuickConfigTemplates/blob/master/Pipfile)
* [See requirements.txt](https://github.com/btr1975/QuickConfigTemplates/blob/master/requirements.txt)

### Some Instructions

* [Wiki](https://github.com/btr1975/QuickConfigTemplates/wiki)

In the Data directory there is a **config.yml** file, this file is used to change directories for the data. It looks
like this.
	
```yaml
--- # Version 1.0.1
config:
  yml_directory: <-- This can be a list if you want multiple directories.  They will be searched in order. First file found wins.
  templates_directory: <-- This can be a list if you want multiple directories.  They will be searched in order. First file found wins.
  output_directory:
  logging_directory:
  logging_level:
```
### Some important notes
If you are planning on compiling with pyinstaller 3.2.1 there is a bug you need to either fix, or download the dev 
version of pyinstaller.

See the details here [pyinstaller github bug #2434](https://github.com/pyinstaller/pyinstaller/issues/2434)

Compiles fine with pyinstaller 3.3.1
