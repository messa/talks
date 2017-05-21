Deployment via _now_ for Javascript and Python in Docker
========================================================

At [Pyvo _Serverless_](https://pyvo.cz/praha-pyvo/2017-05/) Prague Python meetup on May 17 2017

_now_ homepage: [https://zeit.co/now](zeit.co/now)


Installation
------------

    npm install -g now
    
Or follow instructions at https://zeit.co/download


Javascript example
------------------

Create a "hello world" Javascript web app - we will use [next.js](https://github.com/zeit/next.js/) (from the same guys as _now_) because it's easy to use.

- package.json

  ```json
  {
    "dependencies": {
      "next": "^2.3.1",
      "react": "^15.5.4",
      "react-dom": "^15.5.4"
    },
    "scripts": {
      "build": "next build",
      "start": "next start"
    }
  }
  ```

- pages/index.js

  ```javascript
  export default () => <h1>Hello from JS</h1>
  ```

Now :) just run the command:

TODO screenshot


Python Flask example
--------------------

Create a "hello world" Flask web app:

- hello.py

  ```python
  from flask import Flask

  app = Flask(__name__)

  @app.route('/')
  def index():
      return 'Hello from Flask!'
  ```

It will be deployed using Docker, all we need to do is to write a [Dockerfile](https://docs.docker.com/engine/reference/builder/):

- Dockerfile

  ```Dockerfile
  FROM python:3.5

  RUN python3 -m venv venv 
  RUN venv/bin/pip install flask gunicorn

  COPY hello.py .

  EXPOSE 8000

  CMD ["venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "hello:app"]
  ```


Again, deploy with a single command `now`:

TODO screenshot

      
      
