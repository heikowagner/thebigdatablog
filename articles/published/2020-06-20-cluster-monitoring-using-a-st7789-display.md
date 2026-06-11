---
categories:
- All Articles
- Hardware
date: '2020-06-20'
slug: cluster-monitoring-using-a-st7789-display
status: publish
tags: []
title: Cluster Monitoring using a ST7789 Display
wp_id: 2283
wp_modified: '2023-10-01T10:11:32'
---

In the articles [Kuberentes at an OrangePi](https://www.thebigdatablog.com/kubernetes-and-docker-running-at-an-orangepi/) and [Setting up the OrangePi](https://www.thebigdatablog.com/1-setting-up-the-orangepi/) it was described how I build my toy cluster. Meanwhile the cluster received some updates. Two more nodes were added, a Raspberry Pi 3 B+ and a Orange Pi One Plus. Outside temperature and humidity is now measured with a DHT22 sensor. As an NFS storage for persistent volumes I also added a 500GB HDD (leftover from replacing the HDD in my PS4 with an SSD). Finally a 12cm cooler running at 5 V now keeps the cluster temperature low. In addition I added a ST7789 Display to show the cluster status as well as node health and temperature. This article will cover how to connect the display to the cluster and how to manage the communication between the cluster nodes using [DeamonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/).

## 1. Connecting the Display

To display the current status of the cluster a [waveshare ST7789](https://www.amazon.de/Waveshare-2inch-LCD-Module-Communicating/dp/B081NBBRWS/ref=sr_1_13?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1QU8IVS6ETWF&dchild=1&keywords=waveshare+display+raspberry+pi&qid=1590821907&sprefix=waveshare+display%2Caps%2C160&sr=8-13) with 2 inch size is chosen. This display is then connected to the master-node using the following wiring:

\
![](https://www.thebigdatablog.com/wp-content/uploads/2020/05/2inch-LCD-Module-3.jpg)

Source: [https://www.waveshare.com/wiki/2inch\_LCD\_Module](https://www.waveshare.com/wiki/2inch_LCD_Module?Amazon)\

Communication with the display is handled using python and the [spidev](https://pypi.org/project/spidev/) package.

## 2. Using a simple REST Endpoint to gather data

Communication within the cluster is easy. At the master-node a [container with a REST API](https://github.com/heikowagner/temperaturemonitor_reciever) will be deployed which will trigger the display. At each node we will deploy a [small container](https://github.com/heikowagner/temperaturemonitor_sender) that frequently sends the current temperature to the REST endpoint. For the sake of simplicity this example is kept as simple as possible, but can easily be extended if necessary. The code can be found in the corresponding git repos (see links) while the compiled images are available due to dockerhub [here](https://hub.docker.com/repository/docker/iefak01/temperaturemonitor_sendedr) (sender) and [here](https://hub.docker.com/repository/docker/iefak01/temperaturemonitor_reciever) (reciever).

To build the images it is useful to have a development PI, since the images have to be build using arm architecture. Alternatively emulation, for example with Qemu, can be used. Pushing the Images to dockerhub is straightforward

```
docker tag git_reciever:latest &lt;your-repo>/temperaturemonitor_reciever:latest
docker push &lt;your-repo>/temperaturemonitor_reciever:latest
docker tag git_sender:latest &lt;your-repo>/temperaturemonitor_sender:latest
docker push &lt;your-repo>/temperaturemonitor_sender:latest
```

## 3. Setup a DeamonSet to measure node temperature

First we will label the node where the display was connected. Labels are useful to control where certain pods are deployed. Since we want the plot controlling the display to be deployed at the pod where the display is installed, labels are necessary for our purpose. To see all labels assigned to far use

```
kubectl get nodes --show-labels
```

To add a new label to a node

```
kubectl label nodes &lt;your-node-name> display=true
```

Next we create a namespace. In fact creating an own namespace is optional. However namespaces help to structure the cluster and also add a bit of security since we can control which pods have access to the ClusterIP Service used to communicate between the pods. We will create a namespace with the name “disp-monitoring” with

```
kubectl create namespace disp-monitoring
```

To switch to this namespace type

```
kubectl config set-context --current --namespace disp-monitoring
```

With all the infrastructure set up we can deploy our sensor-display deployment using this deployment yaml

```
#apiVersion: v1
#kind: Namespace
#metadata:
#  name: disp-monitoring
#  labels:
#    apps: web-based
#  annotations:
#    type: monitor
#---
apiVersion: v1
kind: Service
metadata:
  name: svc-monitor
  namespace: disp-monitoring
spec:
  selector:
    env: display
  ports:
    - protocol: TCP
      port: 65432
      targetPort: 65432
---
apiVersion: v1
kind: Pod
metadata:
  name: receiver
  namespace: disp-monitoring
  labels:
    env: display
spec:
  containers:
  - image: &lt;your-repo>/temperaturemonitor_receiver:latest
    securityContext:
      privileged: true
    name: receiver
    ports:
    - containerPort: 65432
  nodeSelector:
    display: "true"
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sender
  namespace: disp-monitoring
spec:
  selector:
    matchLabels:
      name: sender
  template:
    metadata:
      labels:
        name: sender
    spec:
      tolerations:
      # this toleration is to have the daemonset runnable on master nodes
      # remove it if your masters can't run pods
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: sender
        image: &lt;your-repo>/temperaturemonitor_sender:latest
        env:
        - name: RECEIVERIP
          value: svc-monitor
```

To deploy the app directly out of my git repo, simply execute

```
kubectl apply -f https://raw.githubusercontent.com/heikowagner/temperaturemonitor_reciever/master/deployment.yaml
```