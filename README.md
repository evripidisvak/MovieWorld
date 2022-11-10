# MovieWorld
## How to run this project

Make sure you have installed Python in your computer

Navigate and open a terminal in a folder in your computer.

Clone the repository.
```
git clone https://github.com/evripidisvak/MovieWorld.git
```

Navigate in the created folder.
```
cd MovieWorld
```

Create a virtual enviroment.
```
python3 -m venv env
```

Activate the virtual enviroment.
```
source env/bin/activate
```
Install all the required packages.
```
pip install -r requirements.txt
```

Navigate in the project folder.
```
cd MovieWorld
```

Run the tests to ensure that everything works as expected.
```
python manage.py  test
```

Start the development server.
```
python manage.py runserver
```

Open a browser at ```http://127.0.0.1:8000/```


Demo credentials:

Admin account. You can also access the backend at ```http://127.0.0.1:8000/admin```

```
admin
123456
```

Regular user.
```
user1
xewvXAUpkr7yF8e

```