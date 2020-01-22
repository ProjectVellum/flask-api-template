Flask Api Template (fat) is a Flask-based basic Rest implementation with the intention
of being inherited by other Rest-based applications. It helps save time implementing
the basic, routine Rest server setup, e.g. starts server, find blueprints, handles
config file and etc.

![](https://github.com/ProjectVellum/flask-api-template/workflows/install_and_unittests/badge.svg)

### Ways to Install


##### PIP3

Make sure pip3 is installed
```
  sudo apt install python3-pip
```

Clone and pip install from source

```
  git clone git@github.hpe.com:atsugami-kun/flask-api-template.git
  cd flask-api-template
  pip3 install -e .
  pip3 install -r requirements.txt
```

##### Raw source

Create a symlink from the cloned project into python3 dist-packages

```
  git clone git@github.hpe.com:atsugami-kun/flask-api-template.git
  sudo ln -s $PWD/flask-api-template /usr/lib/python3/dist-packages/flask_fat
```


### How To Use

To create a Flask-based server using flask_fat, you need to create a class that inherits from flask_fat.

```
import flask_fat


class CustomClass(flask_fat.APIBaseline):

    def __init__(self, cfg, **kwargs):
        super().__init__(cfg, **kwargs)

def main(args=None):
    args = {} # could be command line parsed arguments or whatever needed to pass to the CustomClass
    mainapp = CustomClass('./config', **args)
    if not args.get('dont_run', False):
        mainapp.run()
    return mainapp


if __name__ == '__main__':
    main()
```

Blueprint implementation example can be found in this project at:

https://github.hpe.com/atsugami-kun/flask-api-template/blob/master/flask_fat/blueprints/example/blueprint.py


For a "real life" example project look over there:

https://github.hpe.com/atsugami-kun/redfisher/tree/master/redfisher


### Logging Configuration

By default, this API use ./logging.yaml to configure its logging object that will Only log to Stdout and will not log into file. A yaml example with the file handler can be found [in this article](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/).

Note, there is a hard requirement for the yaml to have a FlaskFatLog logger in the "loggers" attribute:

```
loggers:
  FlaskFatLog:
    level: DEBUG
    handlers: [stdout_handler, info_file_handler]
```

If you wish to add more and/or different "loggers", then you will need to override the "def logging(self)" property of the [APIBaseline](https://github.com/ProjectVellum/flask-api-template/blob/master/flask_fat/baseline.py) class.

### Ways to Build/Package this source

##### pip3 build

To build/rebuild pip3 dist, run the following from the top of the project (where setup.py is):
```
    python3 setup.py sdist bdist_wheel
```

##### .rpm build

```
python setup.py bdist_rpm
```

More info on how to build rpm from python source:


https://docs.python.org/2.0/dist/creating-rpms.html

https://docs.python.org/2/distutils/builtdist.html


##### .deb build

Run from top of the project:
```
    python setup.py --command-packages=stdeb.command bdist_deb
```

For more info:

https://pypi.org/project/stdeb/#quickstart-1-install-something-from-pypi-now-i-don-t-care-about-anything-else
