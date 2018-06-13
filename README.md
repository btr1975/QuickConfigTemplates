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
* [Directions](https://github.com/btr1975/QuickConfigTemplates/blob/master/Docs/Directions.txt)
* [YAML Format](http://yaml.org/)
* [Jinja2 Template Language](http://jinja.pocoo.org)
* [Example Configs](https://github.com/btr1975/QuickConfigTemplates/tree/master/Docs/Examples)

### Version 1.0.3.prod information

* Python: 3.5.2

### Version 1.0.4.prod information

* Added in requirement for persistentdatatools==2.2.7

### Version 1.0.5.prod information

* Added in requirement for persistentdatatools==2.2.8

### Version 1.0.7.prod information

* Added in requirement for Jinja2==2.10
* Added in requirement for py==1.5.2
* Added in requirement for pyaml==17.10.0
* Added in requirement for PyYAML==3.12
* Added in requirement for persistentdatatools==2.2.9
* Added in requirement for ipaddresstools==1.2.8
* Added run_build which now is the command to create a config from YML
* Added pl_create which takes a Prefix-List and converts it to YML, in our format
* Added rm_create which takes a Route-Map and converts it to YML, in our format
* Added acl_create which takes a Route-Map and converts it to YML, in our format, still under development, standard
  seems to work fine, extended has some issue

### Version 1.0.8.prod information

* Now supports a version 2 of the yml file.  This allows you to use multiple groups of devices using different templates.
  Please see the examples in the Docs folder.
* In this version you can have multiple input directories, the "yml_directory" group.
* Added a note key for the yml file, so you can add notes to config sections

### Version 1.0.9.prod information
* You can now include a vars section in your yml to then fill the variable in you yml

```yaml
--- # yml example 1
version: 2
vars:
    var_name1: something1
    var_name2: something2
data:
-   template: iosxr_base.jinja2
    ticket_number: {{ var_name1 }}
    devices:
    -   device:
        -   devicename: {{ var_name2 }}
            management_ip: 1.1.1.1

```

### Version 1.0.10.prod information
* Added more templates for defaults
* Added a rudimentary jinja2 xml for Notepad++

### Version 1.0.11.dev information
* Added some custom [Jinja2 filters](http://jinja.pocoo.org/docs/2.10/templates/) for use in templates to check for correct data see [Wiki](https://github.com/btr1975/QuickConfigTemplates/wiki/Custom-Jinja2-Filters-to-use-in-Templates) for filters

### Requirements
* Jinja2==2.10
* MarkupSafe==1.0
* py==1.5.2
* pyaml==17.10.0
* pytest==3.3.1
* PyYAML==3.12
* persistentdatatools==2.2.9
* ipaddresstools==1.2.8

### Some instructions

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
