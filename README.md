# Python Script: QuickConfigTemplates

## Created By: Benjamin P. Trachtenberg

### Contact Information:  e_ben_75-python@yahoo.com
### If you have any questions e-mail me

### LinkedIn: [Ben Trachtenberg](https://www.linkedin.com/in/ben-trachtenberg-3a78496)
### Docker Hub: [Docker Hub](https://hub.docker.com/r/btr1975)

### About

This script is for simple config templates, to make lif easier on admins/engineers

### Version 1.0.3.prod information

* Python: 3.5.2

### Version 1.0.4.prod information

* Added in requirement for persistentdatatools==2.2.7

### Version 1.0.5.prod information

* Added in requirement for persistentdatatools==2.2.8

### Requirements
* Jinja2==2.9.6
* MarkupSafe==1.0
* py==1.4.34
* pyaml==16.12.2
* pytest==3.1.3
* PyYAML==3.12
* persistentdatatools==2.2.8

### Some instructions

In the Data directory there is a **config.yml** file, this file is used to change directories for the data. It looks
like this.

	
```yaml
config:
  yml_directory:
  templates_directory: <-- This can be a list if you want multiple directories.  They will be searched in order.
  output_directory:
  logging_directory:
  logging_level:
```

### Some important notes
If you are planning on compiling with pyinstaller 3.2.1 there is a bug you need to either fix, or download the dev 
version of pyinstaller.

See the details here [pyinstaller github bug #2434](https://github.com/pyinstaller/pyinstaller/issues/2434)