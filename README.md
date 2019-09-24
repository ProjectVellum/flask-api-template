Flask Api Template (fat) is a Flask-based basic Rest implementation with the intention
of being inherited by other Rest-based applications. It helps save time implementing
the basic, routine Rest server setup, e.g. starts server, find blueprints, handles
config file and etc.


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

###### TODO (currently unknown)