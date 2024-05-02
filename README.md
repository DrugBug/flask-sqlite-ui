### INSTALLATION INSTRUCTIONS ###
This assignment was built using Python 3.10 (Flask & SQLAlchemy).
1. Clone this repository.
2. Enter the main directory (where the `Dockerfile` is found) and run `docker build --tag cellosign:latest .` to build the image.
3. Run `docker run -d -p 5000:5000 cellosign:latest` to run the service.
4. You can now access the web service by browsing the following url: http://127.0.0.1:5000 (http://localhost:5000)
