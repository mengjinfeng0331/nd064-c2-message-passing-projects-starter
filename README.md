# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Goal
You work for a company that is building a app that uses location data from mobile devices. Your company has built a [POC](https://en.wikipedia.org/wiki/Proof_of_concept) application to ingest location data named UdaTracker. This POC was built with the core functionality of ingesting location and identifying individuals who have shared a close geographic proximity.

Management loved the POC so now that there is buy-in, we want to enhance this application. You have been tasked to enhance the POC application into a [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) to handle the large volume of location data that will be ingested.

To do so, ***you will refactor this application into a microservice architecture using message passing techniques that you have learned in this course***. It’s easy to get lost in the countless optimizations and changes that can be made: your priority should be to approach the task as an architect and refactor the application into microservices. File organization, code linting -- these are important but don’t affect the core functionality and can possibly be tagged as TODO’s for now!

### Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0
5. [Install helm](https://helm.sh/docs/intro/quickstart/) 

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`. 
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps
#### 1. start the kafka
Kafka is the message queue for collecting the user location data. 
To setup kafka queue, needs to install helm first.

    $ helm version # check helm is installed
    $ helm repo add bitnami https://charts.bitnami.com/bitnami
    $ helm repo update

    $ helm install sample bitnami/kafka \
     --set volumePermissions.enabled=true \
     --set zookeeper.volumePermissions.enabled=true 

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    sample-kafka-0.sample-kafka-headless.default.svc.cluster.local:9092

After a while, check that kafka is running in the kubernetes cluster
``` shell 
$ kubectl get pods
NAME                                       READY   STATUS    RESTARTS   AGE
sample-zookeeper-0                         1/1     Running   0          3d
sample-kafka-0                             1/1     Running   1          3d
```

#### 2. Person service
Person service is responsible for creating new user and retrieving existing user data.
To deploy person service, go to the person_api folder and apply the deployment files
``` shell
$ cd modules/person_api
$ kubectl apply -f deployment/
```

Wait for the deployments to become ready and populate the person-postgre database
You need to find the pod name for your postgre db for person 
``` shell

$ kubectl get pods
NAME                                       READY   STATUS    RESTARTS   AGE
sample-zookeeper-0                         1/1     Running   0          3d
sample-kafka-0                             1/1     Running   1          3d
postgres-person-6f469db6cc-qrcvv           1/1     Running   0          3d

## extract the postgre-person pod name (postgres-person-6f469db6cc-qrcvv) from above and put it in below
sh /scripts/run_db_command.sh <POSTGRES_PERSON_POD_NAME>

```

Finally, check if the person api service is running by http://localhost:30001/api/persons, and you should see something like below
``` shell
$ curl http://localhost:30001/api/persons
[{"company_name": "Alpha Omega Upholstery", "first_name": "Taco", "last_name": "Fargo", "id": 5}, {"company_name": "USDA", "first_name": "Frank", "last_name": "Shader", "id": 6}, {"company_name": "Hampton, Hampton and McQuill", "first_name": "Pam", "last_name": "Trexler", "id": 1}, {"company_name": "Paul Badman & Associates", "first_name": "Paul", "last_name": "Badman", "id": 8}, {"company_name": "The Chicken Sisters Restaurant", "first_name": "Otto", "last_name": "Spring", "id": 9}]

$ curl http://localhost:30001/health
"healthy"

```

#### 3. connection_api
Connection_api would collect person information and location data to find people nearby
To deply connection_api, go to the connection_api folder and apply the deployment files
``` shell
$ cd modules/connection_api
$ kubectl apply -f deployment/
```
Wait for the deployments to become ready and populate the connection-postgre database
You need to find the pod name for your postgre db for location 
``` shell

$ kubectl get pods
NAME                                       READY   STATUS    RESTARTS   AGE
sample-zookeeper-0                         1/1     Running   0          3d
sample-kafka-0                             1/1     Running   1          3d
postgres-person-6f469db6cc-qrcvv           1/1     Running   0          3d
person-api-dc85c7fb7-4zpn4                 1/1     Running   0          3d
postgres-geoconnections-78c489646d-vq67k   1/1     Running   0          46h

## extract the postgre-geoconnection pod name (postgres-geoconnections-78c489646d-vq67k) from above and put it in below
sh /scripts/run_db_command.sh <POSTGRES_DB_POD_NAME>

```
Finally, check if the connection api service is running by 
http://localhost:30002/api/persons/5/connection?start_date=2020-01-01&end_date=2020-12-30&distance=5
and you should see data returned.


#### 4. location_event serivce. 
location-event service collects the mobile location information and put it to a kafka queue and would be processed by the location_API service later on. 
To deploy location_event service, run the following:
``` shell
$ cd modules/location_event
$ kubectl apply -f deployment/
```

#### 5. Location_api service
Location_api service listens to the kakfa queue for location data, and writes to the location database.
To deploy location_api service, run the following:
``` shell
$ cd modules/location_api
$ kubectl apply -f deployment/
```

#### 6. Frontend service.
Frontend serivce would create the UI and allow user interaction with the geoconnection service
To deploy frontend service, run the followings:
``` shell
$ cd modules/frontend
$ kubectl apply -f deployment/
```


### Finally, check all services and deploymets

``` shell

$ kubectl get all
NAME                                           READY   STATUS    RESTARTS   AGE
pod/sample-zookeeper-0                         1/1     Running   0          3d23h
pod/sample-kafka-0                             1/1     Running   1          3d23h
pod/postgres-person-6f469db6cc-qrcvv           1/1     Running   0          3d23h
pod/person-api-dc85c7fb7-4zpn4                 1/1     Running   0          3d23h
pod/postgres-geoconnections-78c489646d-vq67k   1/1     Running   0          2d22h
pod/geoconnections-api-5c5599549b-dpmwb        1/1     Running   0          2d22h
pod/location-event-api-7dfbcbf74c-dzqmw        1/1     Running   0          2d22h
pod/location-api-76bd67bd4c-llxks              1/1     Running   0          2d21h
pod/udaconnect-app-55d5f89756-zv96s            1/1     Running   0          2d

NAME                                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/kubernetes                  ClusterIP   10.43.0.1       <none>        443/TCP                      3d23h
service/sample-kafka-headless       ClusterIP   None            <none>        9092/TCP,9093/TCP            3d23h
service/sample-zookeeper-headless   ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP   3d23h
service/sample-zookeeper            ClusterIP   10.43.94.144    <none>        2181/TCP,2888/TCP,3888/TCP   3d23h
service/sample-kafka                ClusterIP   10.43.8.135     <none>        9092/TCP                     3d23h
service/person-service              NodePort    10.43.146.139   <none>        5000:30001/TCP               3d23h
service/postgres-person             NodePort    10.43.162.184   <none>        5432:30481/TCP               3d23h
service/postgres-geoconnections     NodePort    10.43.97.33     <none>        5432:31564/TCP               2d22h
service/geoconnections-api          NodePort    10.43.186.156   <none>        5000:30002/TCP               2d22h
service/location-event-service      NodePort    10.43.134.158   <none>        5005:30003/TCP               2d22h
service/location-service            NodePort    10.43.75.198    <none>        9092:32388/TCP               2d21h
service/udaconnect-app              NodePort    10.43.168.176   <none>        3000:30000/TCP               2d

NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/postgres-person           1/1     1            1           3d23h
deployment.apps/person-api                1/1     1            1           3d23h
deployment.apps/postgres-geoconnections   1/1     1            1           2d22h
deployment.apps/geoconnections-api        1/1     1            1           2d22h
deployment.apps/location-event-api        1/1     1            1           2d22h
deployment.apps/location-api              1/1     1            1           2d21h
deployment.apps/udaconnect-app            1/1     1            1           2d

NAME                                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/postgres-person-6f469db6cc           1         1         1       3d23h
replicaset.apps/person-api-dc85c7fb7                 1         1         1       3d23h
replicaset.apps/postgres-geoconnections-78c489646d   1         1         1       2d22h
replicaset.apps/geoconnections-api-5c5599549b        1         1         1       2d22h
replicaset.apps/location-event-api-7dfbcbf74c        1         1         1       2d22h
replicaset.apps/location-api-76bd67bd4c              1         1         1       2d21h
replicaset.apps/udaconnect-app-55d5f89756            1         1         1       2d

NAME                                READY   AGE
statefulset.apps/sample-zookeeper   1/1     3d23h
statefulset.apps/sample-kafka       1/1     3d23h

```


To simulate a mobile location update, you could follow the steps below:

``` shell
## first need to find the pod name for the location-event 

$ kubectl get pods  -o=custom-columns=NAME:.metadata.name | grep location-event

location-event-api-7dfbcbf74c-dzqmw

## next use the location-event name from above 
$ kubectl exec -it [location-event POD NAME] -- sh

## run the python script and you should see the following entry being created

$ python grpc_client_test.py

stub1 create for  id: 34567
person_id: 12
longitude: "-100"
latitude: "200"
creation_time: "2020-03-12"

stub2 create for  id: 3412567
person_id: 123
longitude: "1040"
latitude: "20"
creation_time: "2021-04-22"
```

These pages should also load on your web browser:
* `http://localhost:30001/` - OpenAPI Documentation
* `http://localhost:30001/api/` - Base path for API
* `http://localhost:30000/` - Frontend ReactJS Application
