## <a name="model-deployment">Model Deployment</a>
- **General Info**  

The project aimed to demonstrate how ML model can be prepared for deployment in two modes: *online* and *batch*. For that purpose pretarined `RestNet50` model (with`imagenet` weights) taken to classify two different objects (*cars* and *buses*). The process of model prediction can be done as REST (used **Flask**) or scheduled pipeline (used **cron**) and the model output saved desired directories.

- **Project Structure**

The project can be logically divided into 3 parts:
1. `/src` folder containes all the *code*, *scripts*, *dockerfiles* that necessary for the model deployment preparation.
2. `/tests` contains test that checks input/ output flow behaving correctly. 
3. `pyproject.toml` and `LICENSE` files can be used to package the project.
----
- **Quick Instructions**

Clone the repo, go `/Module5-Model_Deployment` module:
```bash
git clone https://github.com/khazratoff/MLE_HWs.git
cd Module5-Model_Deployment
```

**Requirement: `gdown` package should be installed to gather inference data*. So let's install using **pip** (Choose the version as shown below other newer versions will not work):
```bash
pip install down==4.6.1
```

Now let's download inference data:
```bash
python src/ICMD/data_loader.py
```
Script downloads the data and places it in `resources` folder for further processing.

i. Now we are ready to inference our model. So let's start with *online* mode that uses **Flask** to create REST API.
1. Create a Docker image:
```bash
docker build -f src/ICMD/online/Dockerfile -t rest_model_image . 
```
2. Run the instance of that image:
```bash
docker run --name modelapi -v $(pwd)/resources:/app/resources rest_model_image  
```
*The container builds a Flask server that's ready to listen a request. In our case, the response is nothing but an image. So let's test a server by providing a sample image. using `curl`*

3. Install `curl` which is not installed by default and check whether the server running. For that we need to `exec` the current running container:
```bash
docker exec -it modelapi /bin/bash
apt-get install curl
curl -X GET 'http://localhost:5000/'
```
4. Test a server by giving sample image as request:
```bash
curl -X POST -F image=@car.jpeg 'http://localhost:5000/predict'
```
*You can get a prediction as a list with probabilty*

5. Now let's do the model inference on newly downloaded data in running container.
```bash 
python online/run_inference.py
```
*After successfull run you'll get a predictions in `restAPI_predictions.csv` file in `/resources/output/` folder which is mounted with local file system so that easily accessible.*

ii. Now turn to *batch* mode. For scheduling `cron` tool used with the expression `* * * * *` means that model inferencing should be done in every minute (it's because not to waste a time with waiting and the project is just for simulation not for real-world scenario)

1. For batch, create a Docker image:
```bash
 docker build -f src/ICMD/batch/Dockerfile -t batch_model_image .
 ```
2. Run the instance:
```bash
docker run -d -v $(pwd)/resources:/app/resources batch_model_image
```
- *After successful run, container does inferencing in every minute and stores new predictions as `batch_predictions.csv` in `/resources/output/` folder*
- In addition, *Dockerfile* will be created for online inferencing in the same folder.

iii. Packaging the project:
1. Upgrade the *pip* and *build*:
```bash 
python -m pip install --upgrade pip
python -m pip install --upgrade build
```
2. Run the command:
```bash
python -m build
```

>That's all for now, I am looking forward to your feedback for further development

