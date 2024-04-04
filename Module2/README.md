## <a name="container">Containerization</a>
In this module, the main goal was to create a development environment that sufficient for effective iterations (version control, variables, environment management) with the help of Docker on top of the Linux. In my case, my aim was to create (or install any pretrained) ML model that trains on data, gives predictions as an API and what's more important is the whole process should be run in the isolated container (development environment) that built on the Linux image.
But before diving into the project itself the question arises: 
> *"Why do we use docker, why do we need such separate environments (virtual env, python venv, etc)"*
- *The best possible answer would be: Docker and virtual envs provides benefits such as isolation, reproducibility, dependency management, portability, scalability, environment consistency, and security.* 

> Could you explain why do you need PYTHONUNBUFFERED env setted?
- *By default, Python buffers the output when it's connected to a terminal, which means it may not print the output immediately. This buffering behavior can cause delays in seeing the output, especially in containerized environments like Docker. Setting PYTHONUNBUFFERED=1 disables output buffering, ensuring that the output from your Python application is immediately printed to the Docker logs.*
### Project Overview and Quick Instructions
All necessary files and code for this module can be found Module2 directory includes `Dockerfile` ,`requiremenets.txt` files at the root and `app.py` which is main script of the project in `/src` directory.
<p>Now let's go through the step-by-step instructions on how all works

- Clone this repo to your local machine using this command: 

```bash
git clone https://github.com/khazratoff/MLE_HWs.git
```
- Start the Docker engine using this command (in MacOS):
```bash
open -a Docker.app
```
- Go to the `/Module2` directory and run this command to build an image:
```bash
docker build -t model-api-image .
```
- Now run the container using this command (includes `-v` flag that mountes `/resources` folder and syncs all changes between local and container)<br>
**`/resources` folder contains all the data, trained models and model predictions*.
```bash
docker run -it -v $(pwd)/resources:/app/resources model-api-image /bin/bash
```
- Now inside the container run this command to preprocess and split data into training and test parts before feeding it to ML algorithm:
```bash
python3 src/data_loader.py
```
- Run the actual main file that trains the model and creates small web service to work with model:
```bash
python3 src/main.py
```
- After successfull run we have running web service inside the container, we can check it with `curl` command. Now open another shell and interact running container using `exec` command:
```bash
docker exec -it <name_of_running_container> /bin/bash
```
- Check whether the server is working:
```bash
curl localhost:8000/info
```
- If HTTP status is 200 then we are ready for testing our model with some test input. Give some value instead of 0's and check for model's output:
```bash
curl -X 'POST' \
  'http://localhost:8000/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sepal_length": 0,
  "sepal_width": 0,
  "petal_length": 0,
  "petal_width": 0
}'
```
