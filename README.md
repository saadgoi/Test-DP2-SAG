![Logo](https://n3m5z7t4.rocketcdn.me/wp-content/plugins/edem-shortcodes/public/img/logo-Edem.png)
# IoT Serverless real-time architecture
Data Project 2 | EDEM 2022/2023

## Introdution
### Case description
**Company Name** is a provider producing sugar. One of its many challenges is identifying failures in the production as soon as possible in order to reduce the time-out of their machines. To achieve this challenge, they have launched with IoT sensors  equipped machines to monitor the **temperature** and **absolute pressure** in order to regulate the optimal conditions for the production.

### Business challenge
- You must think of an IoT product, develop it, simulate its use and present it as SaaS.
- The solution must be scalable, open source and cloud.


## Data Architecture & Setup 
### Data Architecture
<img src="00_Img/dp2_arch.png" width="700"/>

### Google Cloud Platform (GCP)
- [Google Cloud Platform - Free trial](https://console.cloud.google.com/freetrial)
- Clone this **repo**
- For this Demo, we will be working on a **Cloud Shell**.

### GCP Components being used in this project
- IoT Core
- Pub/Sub
- Dataflow
- BigQuery
- Data Studio
- Cloud Function
- Cloud Firestore

### Setup Requirements
- Enable required *Google Cloud APIs* by running the following commands:

```
gcloud services enable dataflow.googleapis.com
gcloud services enable cloudiot.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```
- Create Python environment
```
virtualenv -p python3 <ENVIRONTMENT_NAME>
source <ENVIRONMENT_NAME>/bin/activate
```
- Install python dependencies by running the following command:

```
pip install -U -r setup_dependencies.txt
```

## PubSub
First of all, we will create two **Topics** and their default **Subscriptions**.

- Go to Cloud Console [PubSub](https://console.cloud.google.com/cloudpubsub) page. 
- Click **Create Topic**, provide a unique topic name and check **add default subscription** option. 

Both Topics and subscriptions are needed in the following steps in order to create the Data pipeline.

## Cloud Storage

Go to Cloud Console [Cloud Storage](https://console.cloud.google.com/storage) page.

- Create a **bucket** specifying a global unique name. This bucket will be used to store Dataflow Flex template.

## IoT Core

For this demo, we will use Cloud Shell as an IoT data simulator.

- Go to Cloud Console [IoT Core](https://console.cloud.google.com/iot) page.
- Create an IoT Registry by choosing one of the PubSub Topics created before.
- Go to Cloud Shell and generate a **RSA key with self-signed X509 certificate**. more [info](https://cloud.google.com/iot/docs/how-tos/credentials/keys#generating_an_rsa_key)
- Once you have both registry and RSA key created, register a device and upload *rsa_cert.pem* file in *authentication* section.

Now, we have linked our device (Cloud Shell) with IoT Core.

<img src="00_DocAux/iot_ui.PNG" width="700"/>

## BigQuery

- Go to Cloud Console [BigQuery](https://console.cloud.google.com/bigquery) page.
- Create a **BigQuery Dataset** by specifying EU as data location.
- Nothing else will be required as BigQuery table will be created by Dataflow Pipeline.

## Dataflow

- Go to [Dataflow folder](https://github.com/jabrio/Serverless_EDEM/tree/main/02_Dataflow) and follow the instructions placed in **edemDataflow.py** file in order to processing the data by Beam pipeline.
- In this demo, we will create a **Dataflow Flex Template**. More [info](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates).
- You have the files needed in Dataflow folder (*Dockerfile* and *requirements.txt*).
- [Package your python code into a Docker image](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates#python_only_creating_and_building_a_container_image) and store it in Container Registry. You can do this by running the following command:

```
gcloud builds submit --tag 'gcr.io/<YOUR_PROJECT_ID>/<YOUR_FOLDER_NAME>/<YOUR_IMAGE_NAME>:latest' .
```
- [Create Dataflow Flex Template](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates#creating_a_flex_template) from Docker image:

```
gcloud dataflow flex-template build "gs://<YOUR_BUCKET_NAME>/<YOUR_TEMPLATE_NAME>.json" \
  --image "gcr.io/<YOUR_PROJECT_ID>/<YOUR_FOLDER_NAME>/<YOUR_IMAGE_NAME>:latest" \
  --sdk-language "PYTHON" 
```

- Finally, run a [Dataflow job from template](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates#running_a_flex_template_pipeline):

```
gcloud dataflow flex-template run "<YOUR_DATAFLOW_JOB_NAME>" \
    --template-file-gcs-location "gs://<YOUR_BUCKET_NAME>/<YOUR_TEMPLATE_NAME>.json" \
    --region "europe-west1"
```

<img src="00_DocAux/dataflow_ui.PNG" width="700"/>

## Send data from device

- Go to [IoTCore folder](https://github.com/jabrio/Serverless_EDEM/tree/main/01_IoTCore) and run the following command in order to start generating data.

```
python edemDeviceData.py \
    --algorithm RS256 \
    --cloud_region europe-west1 \
    --device_id <YOUR_IOT_DEVICE_NAME> \
    --private_key_file rsa_private.pem \
    --project_id <YOUR_PROJECT_ID> \
    --registry_id <YOUR_IOT_REGISTRY>
```

## Verify data is arriving and visualize them with Data Studio

- Go to [BigQueryUI](https://console.cloud.google.com/bigquery) and you should see your bigquery table already created.

<img src="00_DocAux/bq_ui.PNG" width="700"/>

- Go to [**Data Studio**](https://datastudio.google.com/). Link your BigQuery table.
- Create a Dashboard as shown below, which represents temperature and humidity of the device.
<img src="00_DocAux/Dashboard.PNG" width="700"/>

# Part 02: Event-driven architecture with Cloud Functions

- Go to [CloudFunctions folder]() and follow the instructions placed in edemCloudFunctions.py file.
- Go to Cloud Console [Cloud Functions](https://console.cloud.google.com/functions) page.
- Click **Create Function** (europe-west1) and choose **PubSub** as trigger type and click **save**.
- Click **Next** and choose **Python 3.9** as runtime.
- Copy your code into Main.py file and python dependencies into requirements.txt.
- when finished, Click **deploy**.
- If an aggregate temperature by minute is out-of-range, **a command will be thrown to the device and its config will be updated**. You can check that by going to *config and state* tab in IoT device page.
- Useful information: [IoT Core code samples](https://cloud.google.com/iot/docs/samples)

# Videos
- [IoT Real-time Serverless architecture Part 01](https://www.youtube.com/watch?v=gXngs3pTYJ8)
- [IoT Real-time Serverless architecture Part 02](https://www.youtube.com/watch?v=mh8kNW1OOAU)

# Libraries 

**datetime**: Used to create and manipulate date/time objects. In our case, returning the exact time at the moment of execution and time zone.

logging: The library is widely used for debugging, tracking changes, and understanding the behavior of a program

**random**: Library used to generate random values, in our case, creating data for our mock sensors.

os: It is a portable way of interacting with the underlying operating system, allowing your Python code to run on multiple platforms without modification.

**ssl**: SSJ stands for Secure Sockets Layer. It is used to stablish a secure encrypted connection between devices over a network where others could be “spying” on the communication.

**time**: A designated library to interact with time, such as the sleep function which we used to set intervals in our data stream.

**json**: As its name says, this is a library we used to work with JSON files. We used to json.dumps to convert/write python objects into a json string.

**api**: Just like the previous library, this library is also quite self-explanatory. As it’s used to interact with APIs, and in our case, to simulate one iterating rows our data.

**jw**: JWT stands for JSON Web Token

**paho.mqtt**: MQTT is a publish/subscribe messaging 

**base64**: Base64 is a method of encoding binary data into ASCII text, so that it can be transmitted or stored in a text-based format.

**argparse**: It helps you write code to parse command-line arguments and options, and provides useful error messages and help text for users. With argparse, you can specify the arguments and options your script should accept, and the module will automatically generate a parser that can interpret the arguments passed to your script.

**uuid**: The uuid library in Python is a module that provides the ability to generate UUIDs (Universally Unique Identifiers), as well as various utility functions for working with UUIDs.

