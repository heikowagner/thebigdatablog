---
categories:
- All Articles
- Fundamentals
- Hardware
date: '2019-09-10'
slug: kubernetes-and-docker-running-at-an-orangepi
status: publish
tags: []
title: Kubernetes at an OrangePi
wp_id: 1194
wp_modified: '2023-10-01T10:11:48'
---

# 1. Install k3s at the OrangePI

In a previous article I explained how to get spark running at an OrangePi to create a toy computing-cluster.  If you look at this [article](https://www.thebigdatablog.com/2-installing-hadoop/) you may agree that this was a really painful setup process. For quite a while now I worked with Kubernetes which makes the deployment process a lot easier using container technology. A big advantage is that Kubernetes takes automatically distributes nodes, for example spark workers, across different machines. Sloppy speaking a container is really close to the concept of an VM, but where each VM comes with an entire OS, Container share these components with the host system. Unfortunately, prior to January 2017 OrangePi Images where based on the Linux-Kernel < 3.4 which lacked features required to run containers on the H3 chipset. Since newer Images are based on kernel >=4.14 it is now possible to install Docker or Kubernetes for example using k3s, which uses containerd (the core of Docker) as container technology.\
To Setup the Pi you have to follow these steps:

- Download the [Armbian Bionic Image](https://www.armbian.com/orange-pi-pc/)
- Install the Image on an SD-Card (for example with [Etcher](https://www.balena.io/etcher/) or see Section 3.1 [here](https://www.thebigdatablog.com/1-setting-up-the-orangepi/))
- Put the SD-Card into the Pi and the connect the device

To connect to the device from the host, for people using Windows 10 I recommend installing the [Linux Bash](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) or Git Bash to follow the next steps.

- Login as root : **`ssh root@ip_of_your_master_device`**
- The Password  is **`1234`**

you are forced to change the password. I changed mine to “orangepi”.

The next step is to change the hostname, this is necessary because k3s will later identify the nodes due to this hostname. I labeled the master as “masterpi” while the nodes where denoted as “nodepi1”, “nodepi2 ” and so on. To change the hostname type **`echo "masterpi" > /etc/hostname`**. In addition you have to replace the “orangepi” entries with “masterpi” in **`sudo nano /etc/host`**. To commit the changes reboot the Pi with **`sudo reboot`**.

Next you have to install the latest k3s Kubernetes cluster on the masterpi:

**`curl -sfL https://get.k3s.io | sh -`**

This may take a while. k3s is now starting and begins to download required images from the Kubernetes registry. To check if the systemd service is running type**`sudo systemctl status k3s`**

## 1.2 Adding more nodes

To add more nodes to your cluster you need to know the token of your master node. To get this token, execute at the master

**`sudo cat /var/lib/rancher/k3s/server/node-token`**

A token might look like *K10ca1b47907be6d5cf91e6e7a29d1d52c9b36c087ca35da3cee2757a9a3507ed5a::node:24af5a7878e575c3f36566a0011395f3*.

Then prepare a second (or third or whatever) device as described above. At each node you have to define the following environment variables based on your actual setup

- `export K3S_URL="https://ip_of_your_master_device:6443"`
- `export K3S_TOKEN="K10ca1b47907be6d5cf91e6e7a29d1d52c9b36c087ca35da3cee2757a9a3507ed5a::node:24af5a7878e575c3f36566a0011395f3"`
- `curl -sfL https://get.k3s.io | sh -`

You can now join your node to the cluster this way:

**`sudo k3s agent --server ${K3S_URL} --token${K3S_TOKEN}`**

Well done, you have successfully deployed a mini Kubernetes cluster using OrangePis hardware. You can now check via **`kubectl get nodes`** if all nodes are connected succesfully to the cluster.

## 1.3 Install kubectl on the host

For an easier deployment process we will now install kubectl at our host pc and connect it to our cluster. If you are a Windows user you can download the [binary](https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/windows/amd64/kubectl.exe), as a Linux (Ubuntu, Debian) user you can install kubectl via

```
sudo apt-get update &amp;&amp; sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
```

To connect to your cluster you first have to define the cluster

- `kubectl config set-cluster mycluster --server=https://ip-of-your-master-device:6443 --insecure-skip-tls-verify`
- `kubectl config set-context mycontext --cluster=mycluster --user=default`

Next you have to log in into the master and type **`kubectl config view --raw`** to see the user default and certificate. At the host we will add this user at the end of **`~/.kube/config`.** Finally we have to switch to the created context with **`kubectl config use-context mycontext`**  You are now ready to deploy your first nginx deployment with 3 replica pods from the host with **`kubectl apply -f https://raw.githubusercontent.com/heikowagner/thebigdatablog/master/deployment.yaml`**and check via **`kubectl get po`** if the pods are running. Finally you can connect to your nginx server and see a 404 Page by typing the **`ip_of_your_master_device`** in your browser.