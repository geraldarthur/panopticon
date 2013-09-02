# Panopticon
The Panopticon will read files from your Moves.app JSON export, load them into a MongoDB instance, and then make them available via a JSON API powered by Flask. Make maps or something.


## Requirements
* You have a Mongo DB instance running on the standard port.
* You have a database named ```apps```.

## Bootstrap
* Clone the project and setup your virtualenv.

```
git clone git@github.com:jeremyjbowers/panopticon.git
cd panopticon
mkvirtualenv panopticon
pip install -r requirements.txt
```

* Next, copy your data file from http://moves-export.herokuapp.com/ into the ```data/``` folder with a .json extension.

* Then, run the fab commands to insert the data into MongoDB.

```
fab load_data
```

* Now, run the app and check it out in your web browser at http://127.0.0.1:8000/panopticon/raw/.

```
./app.py
```

Congrats! Now make a map or something.