## <a name="container">Pipelines</a>
- **General Info**  

The project aims to maintain ``data processing pipeline`` using **Apache Airflow** on the *student-perfomance* dataset.   

- **Project Structure**

This module includes python scripts, data and DAG defining scripts. `data_generate.py` file actually splits the dataset into 2 categories respect to the columns: *human factors* and *academic factors* (and *"academic factors data"* treated as external source). In `data_process.py` script processing pipeline defined that Airflow DAG utilize later.


The project consists of 3 main parts:
1. *Scripts that actually processes the data*
2. *DAG that maintain this pipeline*
3. *Saving the processed data into local machine*

-----
- **Quick Instructions**  

1. Clone the repo, go `/Module4` directory:
```bash
git clone https://github.com/khazratoff/MLE_HWs.git
cd Module4-Pipelines
```
2. Build the Docker image:
```bash
docker build -f Dockerfile -t airflow-image . 
```
3. Run the instance of that image:
```bash
docker run --detach -v $(pwd)/data:/opt/airflow/data -p 8080:8080 airflow-image
```
- *Container runs with `-p 8080:8080` flag to make it accessible to the airflow-ui within local computer*
- *-`-v` flag used to mount data folder to get processed data*
4. Go to [**airflow-ui**](http://localhost:8080)
5. Login (username:`admin`,password:`admin`)
6. You can see ``Student_Performance_DAG`` in the DAGs list (if no just wait a little bit...). You can manually trigger this DAG by run button but actually this DAG runs automatically.
7. Check your `/data` folder.
> After successfull run make sure that `/processed/` folder created in the data directory that contains processed clean data
If you want to see what's going behind the scenes run ```docker logs <container-name>```