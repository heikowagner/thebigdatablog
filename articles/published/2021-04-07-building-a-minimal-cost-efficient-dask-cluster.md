---
categories:
- All Articles
- Cluster
- Kubernetes
- Python
date: '2021-04-07'
slug: building-a-minimal-cost-efficient-dask-cluster
status: publish
tags: []
title: Building a minimal, cost efficient Dask cluster
wp_id: 3039
wp_modified: '2023-10-01T10:11:13'
---

In this article we will show a way to do high performance parallel computing at a Kubernetes cluster using task. A primary focus is that we want to archive the most cost efficient way. To do so we need a very flexible setup that can be scaled up and down on short term. A key requirement is that the container that have to be downloaded need to be small, therefore this article is divided into two sections. A section covering how to build and maintain a minimal Dask docker container for various platforms and how to integrate auto scaling with Kubernetes into a python workflow. The most recent version of the code is available at [GitHub](https://github.com/heikowagner/minimaldask).

[**A python packagethat takes care of a dask kubernetes deployment including a minmal Docker image.**](https://github.com/heikowagner/minimaldask)  \
 <https://github.com/heikowagner/minimaldask>\
 [5](https://github.com/heikowagner/minimaldask/network) forks.\
 [3](https://github.com/heikowagner/minimaldask/stargazers) stars.\
 [1](https://github.com/heikowagner/minimaldask/issues) open issues.\
  Recent commits:

- [additional dask start arguments](https://github.com/heikowagner/minimaldask/commit/7b348776d012c86016c17af186f98f4ba8f6ac4e), Heiko Wagner
- [precommit](https://github.com/heikowagner/minimaldask/commit/4bb1a5f8c0fc1fd613c7177c5b723b597a41bdf7), Heiko Wagner
- [Update \_\_init\_\_.py](https://github.com/heikowagner/minimaldask/commit/5527d371afd0f833efdb56284c2df619a309f876), Heiko Wagner
- [precommit](https://github.com/heikowagner/minimaldask/commit/83982eaac62fe60fbf32e2bdf594d61b7f2dfb94), Heiko Wagner
- [precommit](https://github.com/heikowagner/minimaldask/commit/a973bb75ec95e26defb39e5449a1b2c2446398b0), Heiko Wagner

## 1. Dockerfile

There already exists an [official Dask Docker Image](https://hub.docker.com/u/daskdev). The actual Image size of this image is 212.52 MB, and this image will not run on an arm architecture like Raspberry Pi or Orange Pi. As the interested reader knows, there are several [articles](https://www.thebigdatablog.com/kubernetes-and-docker-running-at-an-orangepi/) in this blog that deal with the construction of an Orange PI cluster. To build a Kubernetes Deployment and corresponding Docker Images that can run on this cluster was therefore a must.

For a minimal container we rely on Alpine Linux as a base image with pre-installed Python.

```
FROM python:3.9.2-alpine3.13

MAINTAINER Heiko Wagner, heikowagner@thebigdatablog.com

RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --update --no-cache py3-pandas@testing && mv -f /usr/lib/python3.8/site-packages/* /usr/local/lib/python3.9/site-packages/

RUN echo "INSTALLING DASK"
RUN apk update \
    && apk add --virtual build-deps gcc musl-dev linux-headers libffi-dev jpeg-dev zlib-dev libjpeg g++ build-base libzmq zeromq-dev\
    && apk add py-psutil libjpeg\
    && pip uninstall -y numpy \
    && pip install numpy \
    && pip install dask[complete] jupyter-server-proxy \
    && apk del build-deps \
    && pip cache purge \
	&& find /usr/local/lib/python3.9/site-packages -follow -type f -name '*.a' -delete \
    && find /usr/local/lib/python3.9/site-packages -follow -type f -name '*.pyc' -delete \
    && find /usr/local/lib/python3.9/site-packages -follow -type f -name '*.js.map' -delete \
    && find /usr/local/lib/python3.9/site-packages/bokeh/server/static -follow -type f -name '*.js' ! -name '*.min.js' -delete

RUN echo "COPY ENTRYPOINT"
COPY entrypoint.sh /usr/local/bin
RUN chmod 755 /usr/local/bin/entrypoint.sh

#Just in case entrypoint.sh was edited using Windows
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted \
	&& dos2unix /usr/local/bin/entrypoint.sh \
	&& apk del dos2unix

ENTRYPOINT ["entrypoint.sh"]
```

Python packages like Pandas are compiled at runtime, therefore a build environment is required. This build environment is not necessary when running the container in the cluster. There are at least two tricks to handle this problem, one way is to use [multi stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) where you can copy compiled programs from one image to another. We choose the second option. To prevent that the build environment ends up in the final container we create a virtual apk environment called *build-deps*. After the successful installation of Dask this build environment, together with temporary pip files and unneeded *\*.js.map, \*.pyc* files, is then [deleted](https://github.com/heikowagner/minimaldask/blob/master/Dockerfile#L10-L15). Since this is all done in one step, no intermediate stuff ends up in any docker layer.

```
#!/bin/sh

# We start by adding extra apk packages, since pip modules may required library
if [ "$EXTRA_APK_PACKAGES" ]; then
    echo "EXTRA_APK_PACKAGES environment variable found.  Installing."
    apk update
    apk add $EXTRA_APT_PACKAGES
fi

if [ "$EXTRA_PIP_PACKAGES" ]; then
    echo "EXTRA_PIP_PACKAGES environment variable found.  Installing".
    pip install $EXTRA_PIP_PACKAGES
fi


if [ "$WORKER" ]; then
  echo "Worker Node starting"
  dask-worker master-node:$PORT$ARGUMENTS
else
  echo "Master Node starting"
  dask-scheduler --port $PORT$ARGUMENTS --dashboard
fi

# Run extra commands
exec "$@"
```

There is no different image for scheduler and worker. We control purpose using the environment variable **$WORKER** which is used in the [entrypoint](https://github.com/heikowagner/minimaldask/blob/master/entrypoint.sh) to start the appropriate. Besides the user can modify the container behavior using the environment variables.

- **\_\_WPMATH\_0002\_\_EXTRA\_PIP\_PACKAGES** – pip Packages that are installed at container start
- **\_\_WPMATH\_0003\_\_ARGUMENTS** – Extra arguments like memory limit or number of threds. Look [here](https://docs.dask.org/en/latest/setup/cli.html#dask-worker) for a complete list

The final Docker image is [available at DockerHub](https://hub.docker.com/r/iefak01/minimaldask/tags?page=1&ordering=last_updated) (iefak01/minimaldask) and has only between 49MB and 53MB depending on the platform.

## 2. GitHub Actions

DockerHub has a nice autobuild feature, which was already used in [this project](https://www.thebigdatablog.com/cluster-monitoring-using-a-st7789-display/). If DockerHub is connected to a certain GitHub Repo, containing a *Dockerfile*, each time a certain hook is triggered (e.g. merge into master) the image is rebuild. A feature missing at DockerHub is building images for different platforms. All images that where build using DockerHub are running at an amd64 architecture. Since a key requirement of this project is to deliver an image that can be used with an Raspberry or an Orange PI using DockerHub to build the images automatically was not an option. Here GitHub Actions steps in to solve the problem. If you are familiar with Jenkins, you will recognize many similarities. Like Jenkins GitHub Actions uses Pipelines to orchestrate a workflow. This can then be used to automatically perform test based on some trigger or, like in our case, to automatically build docker containers. An advantage of GitHub Actions compared to Jenkins is that the framework is integrated in GitHub, there is no need for an external server, adding further architectural complexity. Based on the [tutorial by Kevin Mansel](https://medium.com/swlh/using-github-actions-to-build-arm-based-docker-images-413a8d498ee) the GitHub Actions [workflow](https://github.com/heikowagner/minimaldask/blob/master/.github/workflows/main.yml) was modified to be able to build containers for arm-v7 (Raspberry Pi), arm64 (Raspberry Pi 4) and amd64. This is possible because of the new docker build routine *buildx*. While previously one have to create a virtual machine for every platform manually, *buildx* automates this out of the box.

```
name: Docker Build/Publish Image 
on:  
  push:    
    branches: [ master ]
    paths:
    - 'entrypoint.sh'
    - 'Dockerfile'
jobs:   
  build:    
    runs-on: ubuntu-18.04    
    env:      
      DOCKER_REGISTRY: docker.io
      DOCKER_IMAGE: iefak01/minimaldask
      DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
      DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}  
      DOCKER_TARGET_PLATFORM: linux/arm/v7,linux/amd64,linux/arm64
    steps:    
    - name: Checkout the code       
      uses: actions/checkout@v1              
    - name: Set up Docker Buildx      
      uses: crazy-max/ghaction-docker-buildx@v1      
      with:        
        buildx-version: latest          
    - name: Prepare      
      if: success()      
      id: prepare      
      run: |        
        echo ::set-output name=docker_platform::${DOCKER_TARGET_PLATFORM}        
        echo ::set-output name=docker_image::${DOCKER_IMAGE}        
        echo ::set-output name=buildx-version::${GITHUB_RUN_NUMBER}        
    - name: Docker Login      
      if: success()      
      run: |        
        echo "${DOCKER_PASSWORD}&quot; | docker login${DOCKER_REGISTRY} --username "${DOCKER_USERNAME}" --password-stdin              
    - name: Run Buildx (push image)      
      if: success()      
      run: |        
        docker login && \
        docker buildx build \
        --platform ${{ steps.prepare.outputs.docker_platform }} \
        --tag ${{ steps.prepare.outputs.docker_image }}:latest \
        --tag ${{ steps.prepare.outputs.docker_image }}:${{ steps.prepare.outputs.buildx-version }} \
        --push .
```

## 3. Kubernetes Deployment

The Kubenetes deployment consists of three scripts. The scripts are usually not executed directly or be templated for a helm chart but are considered as templates so that the dask cluster can directly be deployed and modified using python.

1. service.yaml – a service to connect scheduler and worker. Besides the service serves as an endpoint for our python framework

```
apiVersion: v1
kind: Service
metadata:
  name: master-node
spec:
  type: NodePort
  selector:
    env: sheduler
  ports:
  - protocol: TCP
    port: 8786
    name: sheduler
    targetPort: 8786
    nodePort: 30086
  - protocol: TCP
    name: dashboard
    port: 8787
    targetPort: 8787
    nodePort: 30087

# Connect to Dashboard: 
# kubectl port-forward service/master-node 8787:8787  
# localhost:8787
```

2. sheduler.yaml – a deployment that serves as a master node for the dask cluster

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sheduler
  labels:
    app: minimaldask
spec:
  replicas: 1
  selector:
    matchLabels:
      env: sheduler
  template:
    metadata:
      labels:
        env: sheduler
    spec:
      containers:
        - name: sheduler
          image: iefak01/minimaldask:latest
          ports:
            - containerPort: 8786
            - containerPort: 8787
          env:
          - name: PORT
            value: "8786"
```

3. worker.yaml – a deployment that brings up the workers. With *replica* the number of worker can be controlled

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker
  labels:
    app: minimaldask
spec:
  # modify replicas according to your case
  replicas: 3
  selector:
    matchLabels:
      env: worker
  template:
    metadata:
      labels:
        env: worker
    spec:
      containers:
      - name: worker
        image: iefak01/minimaldask:latest
        env:
        - name: PORT
          value: "8786"
        - name: WORKER
          value: "true"
```

## 4. Python Example

The Idea of the deployment is that we want to use it as cost-efficient as possible. The cluster should only be up and running if necessary. The use case here is that the dask cluster (or at least a big dask cluster) is only is rarely needed. Thus, we want to control the deployment at the same point where the computation is held. in particular in the python script. The implementation is based on the official [python kubernetes api](https://github.com/kubernetes-client/python). Since this api lacks of a function that checks if a deployment is up and running and updates if necessary, a new function *[update\_or\_deploy()](https://github.com/heikowagner/minimaldask/blob/master/src/minimaldask/kubernetes_helper.py#L48-L76)* is introduced.

The cluster is controlled by just two python functions, *start\_dask\_cluster()* and *delete\_dask\_cluster()*.

```
from dask.distributed import Client
import dask.array as da
import subprocess
import re
from minimaldask import start_dask_cluster, delete_dask_cluster

# We determine the ip of the master node using kubectl
p = subprocess.Popen("kubectl cluster-info", stdout=subprocess.PIPE)
kube_conf = p.stdout.read().decode()
master_ip = re.findall(r"//([\s\S]*?):", kube_conf, re.MULTILINE)[0]


def main():
    start_dask_cluster(
        namespace="default", worker_dask_arguments="--nthreads 5"
    )
    print("The Dashboard is available at: http://" + master_ip + ":30087")
    dask_client = Client(master_ip + ":30086")  # noqa

    # Run the computation at the cluster
    x = da.random.random((10000, 10000), chunks=(1000, 1000))
    y = x + x.T
    z = y[::2, 5000:].mean(axis=1)
    print(z.compute())

    delete_dask_cluster(namespace="default")


if __name__ == "__main__":
    main()
```

## 5. Next Steps

- ~~At the moment the Docker Images are build after every push into the master branch, even if the Dockerfile was not modified. The GitHub Actions workflow has to be adjusted that the Image is only rebuild if Dockerfile or entrypoint.sh was changed. Alternatively a rebuild should be triggered with a commit message consisting “rebuild”.~~ Solved in 6,7 in the GitHub Actions Script.
- ~~Python functions to control the dask cluster should be integrated in a package.~~