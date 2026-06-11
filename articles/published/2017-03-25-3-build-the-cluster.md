---
categories:
- All Articles
- Install Spark on a OrangePi PC
- Projects
date: '2017-03-25'
slug: 3-build-the-cluster
status: publish
tags: []
title: 3. Build the Cluster
wp_id: 815
wp_modified: '2023-10-01T10:13:01'
---

### 1. Requirements

We need an SD Card with [Lubuntu, Hadoop and Spark installed](https://www.thebigdatablog.com/2-installing-hadoop/).

### 2. Build the Cluster

#### 2.1 Clone the SD Card

`sudo shutdown 0` of your orangepi and remove the SD Card. If you are using Linux you can be happy since cloning an SD Card is super simple, just execute `dd if=/dev/sdcard1 of=~/sdimage`, `dd if=~/sdimage of=/dev/sdcard2`. If you are a Windows user you can use again [Win32 Disc Imager](https://sourceforge.net/projects/win32diskimager/). Instead of writing we now read out the data from SD Card, to some location. Write just write the saved image to the new SD Card as described in [Section 1](https://www.thebigdatablog.com/1-setting-up-the-orangepi/).

#### 2.2 Configure the Nodes

##### 2.2.1 Set unique static IP Adresses

Because the nodes need to communicate with each other we have to set a for each node static ip address first. For example if we want to have the node the 192.168.1.101 open `sudo nano /etc/network/interfaces`, quote out `source-directory /etc/network/interfaces.d` and insert\
`\
auto eth0\
iface eth0 inet static\
address 192.168.1.101\
netmask 255.255.255.0\
broadcast 192.168.1.255\
gateway 192.168.1.1\
dns-nameservers 192.168.1.1\`. For this example, we will use 192.168.1.101 as master and 192.168.1.102 as slave.

Next we want to map the nodes and avoid an error message IPv6 we will disable IPv6 by opening `sudo nano /etc/sysctl.conf` and adding `\
192.168.1.101 master\
192.168.1.102 slave-1`

# disable ipv6\
net.ipv6.conf.all.disable\_ipv6 = 1\
net.ipv6.conf.default.disable\_ipv6 = 1\
net.ipv6.conf.lo.disable\_ipv6 = 1

##### 2.2.2 Esatablish SSH Connections

Because we do not want to enter the passwords each time the cluster boots, we first want to establish an SSH Connection between the nodes.\
First establish a connection from the master to the master itself `ssh-keygen -t rsa -P ""` and `cat $HOME/.ssh/id_rsa.pub &gt;&gt;$HOME/.ssh/authorized_keys` then connect the local machine `ssh localhost` and establish a connection between master and slave `ssh-copy-id -i $HOME/.ssh/id_rsa.pub hduser@192.168.1.102</code>, <code>ssh-copy-id -i$HOME/.ssh/id_rsa.pub hduser@slave`

##### 2.2.3 Configure Hadoop (ALL Nodes)

First we need decide where to store the data\
`\
sudo mkdir -p /usr/local/hadoop/tmp\
sudo chown hduser:hadoop /usr/local/hadoop/tmp\
sudo mkdir -p /usr/local/hadoop/name\
sudo chown hduser:hadoop /usr/local/hadoop/name/\
sudo mkdir -p /usr/local/hadoop/data\
sudo chown hduser:hadoop /usr/local/hadoop/data\`

**Hint:\**If you want to build a real cluster you might think about using an external drive, then you should use the folder at the harddrive and not the rather small SD Card.

Change to `su hduser`, go to `cd $HADOOP_CONF_DIR` and open `nano core-site.xml` and replace\
`\
<configuration>\
<property>\
<name>fs.default.name</name>\
<value>hdfs://master:54310/</value>\
</property>\
<property>\
<name>hadoop.tmp.dir</name>\
<value>/usr/local/hadoop/tmp</value>\
</property>\
</configuration>`

Next, open `nano hdfs-site.xml` and replace\
`\
<configuration>\
<property>\
<name>dfs.data.dir</name>\
<value>/usr/local/hadoop/data</value>\
<final>true</final>\
</property>\
<property>\
<name>dfs.name.dir</name>\
<value>/usr/local/hadoop/name/</value>\
<final>true</final>\
</property>\
<property>\
<name>dfs.replication</name>\
<value>2</value>\
</property>\
<property>\
<name>dfs.permissions</name>\
<value>false</value>\
</property>\
</configuration>`

The default value of df.replication is 3, however since we build a cluster with 2 nodes we will use 2.

Change back to `su hduser` on the main node\
`hdfs namenode -format`\
Next start the hdfs:\
`\
cd $HADOOP_HOME/sbin\
start-dfs.sh\`

To check your installation go to http://192.168.1.101:50070, if you see something like this then you succeeded.

[![](https://www.thebigdatablog.com/wp-content/uploads/2017/03/sucess-1-300x251.jpg)](https://www.thebigdatablog.com/wp-content/uploads/2017/03/sucess-1.jpg)

#### 3. Configure Spark

First we need to grant some folder permissions at all nodes as the orangepi user `sudo chown hduser:hadoop ./spark-2.1.0-bin-hadoop2.7` and `sudo chmod 750 ./spark-2.1.0-bin-hadoop2.7`. Next we need to edit the configuration file at the master node at in the /opt/spark-2.1.0-bin-hadoop2.7/conf folder by `sudo cp slaves.template slaves` and add the lines\
`\
192.168.1.101\
192.168.1.102\`\
then after `sudo cp spark-env.sh.template spark-env.sh` we need to add the line `SPARK_MASTER_HOST=192.168.1.101` to `sudo nano /etc/spark/conf/spark-env.sh`\
to start the Spark server execute `$SPARK_HOME/sbin/start-all.sh` from the Spark main folder.

To check your installation go to http://192.168.1.101:8080, if everything turns out to be correct you should see something like this: [![](https://www.thebigdatablog.com/wp-content/uploads/2017/03/sucess-300x205.jpg)](https://www.thebigdatablog.com/wp-content/uploads/2017/03/sucess.jpg)Congratulation, you successfully set up an Hadoop/Spark Cluster. In the [next Section](https://www.thebigdatablog.com/4-install-ipython-with-remote-notebook/) we will install some software and carry out the first analysis.