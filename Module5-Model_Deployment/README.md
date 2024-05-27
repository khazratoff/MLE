## <a name="model-deployment">Model Deployment</a>
- **General Info**  

The project aimed to demonstrate how ML model can be prepared for deployment in two modes: *online* and *batch*. For that purpose pretarined `RestNet50` model (with`imagenet` weights) taken to classify two different objects (*cars* and *buses*). The process of model prediction can be done as REST (used **Flask**) or scheduled pipeline (used **cron**) and the model output saved desired directories.

- **Project Structure**

The project can be logically divided into 3 parts:
1. `/src` folder containes all the *code*, *scripts*, *dockerfiles* that necessary for the model deployment preparation.
2. `/tests` contains test that checks input/ output flow behaving correctly. 
3. `setup.py` file can be used to package the project.
----
- **Quick Instructions**

Clone the repo, go `/Module5-Model_Deployment` module:
```bash
git clone https://github.com/khazratoff/MLE_HWs.git
cd Module5-Model_Deployment
```

**Inferencing** *can be done in* **local environment** *and using* **Docker**. *Let's go through one by one.*

1. Running inference in local environment:
    1. Create a virtual environment, let's call it "icmd_env":
    ```bash
    python -m venv icmd_env
    ```
    2. Activate this environment:
    ```bash
   source icmd_env/bin/activate
   ```
   **Use `.` instead of `source` command if you are not using bash shell or another that doesn't support this command*

   3. Setup-tools based installation. Install all necessary dependencies and custom console scripts:
   ```bash
   pip install -e .
   ```
   4. **Inferencing**. Load the data:
   ```bash
   load-data
   ```
   5. Start flask server:
   ```bash 
   start-server
   ```
   6. Run inference online and store results in `/recources/output/` folder.
   ```bash
   run-inference-online
   ```
   7. Schedule batch inferencing (based on crontab) and store results in`/recources/output/`: 
   ```bash
    schedule-batch-inference 
    ```
2. Inferencing using Docker
    1. Create a network called `flask-network`:
    ```bash
    docker network create flask-network 
    ```
    2. Create a server image and client images:
    ```bash
    docker build -f docker/server/Dockerfile -t server-image .
    docker build -f docker/client/Dockerfile -t client-image .
    ```
    3. Run server container:
    ```bash
    docker run --name flask-server --network flask-network -p 5000:5000 server-image
    ```
    4. Run client container:
    ```bash
    docker run -v $(pwd)/resources:/app/resources --network flask-network -e FLASK_SERVER_HOST=flask-server client-image
    ```
    *See the results in `resources` folder*.
    
3. Testing.
```bash 
pytest
```
