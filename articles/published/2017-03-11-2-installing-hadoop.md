---
categories:
- All Articles
- Install Spark on a OrangePi PC
- Projects
date: '2017-03-11'
slug: 2-installing-hadoop
status: publish
tags: []
title: 2. Install Hadoop and Spark
wp_id: 795
wp_modified: '2023-10-01T10:13:06'
---

### 1. Requirements

An Orangepi with Lubuntu running, see this [post](https://www.thebigdatablog.com/1-setting-up-the-orangepi/) for further instructions.

### 2.Install the Components

#### 2.1 Update Java

In fact Hadoop is not necessary for Spark. However, we will later use Hadoop as a storages system for Spark. Access the OrangePi using Keyboard and Monior due to Terminal or SSH using [PuttY](http://www.putty.org/). Login and Password are **orangepi**. Before installing Hadoop we have to make sure that **Oracle Java** is up to date. First visit the [Java Download page](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) and copy the link for the Linux ARM 32 Version. Go to the Download folder with `cd Download` then download the Java installation file with `sudo wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u121-b13/e9e7ea248e2c4826b92b3f075a80e441/jdk-8u121-linux-arm32-vfp-hflt.tar.gz` (replace the file with the actual version if necessary). Next we have to extract the file by `sudo tar -zxvf jdk-8u121-linux-arm32-vfp-hflt.tar.gz`. In the next step we have to install the new jave version, therefore execute `sudo update-alternatives --install /usr/bin/javac javac /home/orangepi/Downloads/jdk1.8.0_121/bin/javac 1`, `sudo update-alternatives --install /usr/bin/java java /home/orangepi/Downloads/jdk1.8.0_121/bin/java 1`, `sudo update-alternatives --config javac`, `sudo update-alternatives --config java`.

#### 2.1 Install Hadoop

We will use Hadoop as an additional user with the name *hduser* in the *hadoop* group. To create this user execute  `sudo addgroup hadoop` , `sudo adduser --ingroup hadoop hduser`, `sudo adduser hduser sudo`. Download Hadoop with `wget ftp://apache.belnet.be/mirrors/ftp.apache.org/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz` and extract the files to the *opt* directory `sudo tar -xvzf hadoop-2.7.3.tar.gz -C /opt/`. Go to the *opt* directory and make the extracted files accessible to the *hduser* `sudo chown -R hduser:hadoop hadoop-2.7.3/`. Then switch to the *hduser*, `su hduser` and add some enviroment variables `nano ~/.bashrc`. Add\
`\
SPARK_HOME=/opt/spark-2.1.0-bin-hadoop2.7\
PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH\
export JAVA_HOME=/home/orangepi/Downloads/jdk1.8.0_121/\
export HADOOP_HOME=/opt/hadoop-2.7.3\
export HADOOP_MAPRED_HOME=$HADOOP_HOME\
export HADOOP_COMMON_HOME=$HADOOP_HOME\
export HADOOP_HDFS_HOME=$HADOOP_HOME\
export YARN_HOME=$HADOOP_HOME\
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop\
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop\
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin` .\
Save and apply the changes with `source ~/.bashrc`. Finally change JAVA\_HOME to `export JAVA_HOME=/home/orangepi/Downloads/jdk1.8.0_121/` in `nano $HADOOP_CONF_DIR/hadoop-env.sh`.\
Thats it, you finally installed Hadoop on your Orangepi. In a next step we have to configure Hadoop for our cluster purposes, this will be the topic of the next post.

To acknowlege the limited resources of the orangepi we have to change some configurations which will prevent a crash of the cluster ([vgl.](http://www.widriksson.com/raspberry-pi-2-hadoop-2-cluster/)). Therefore go to $HADOOP\_HOME/etc/hadoop and rename `cp mapred-site.xml.template mapred-site.xml` and `cp yarn-site.xml.template yarn-site.xml` and edit `nano mapred-site.xmlmapred-site.xml` and instert between <configuration>\
`\
mapreduce.framework.name\
yarn\
mapreduce.map.memory.mb\
256\
mapreduce.map.java.opts\
-Xmx204m\
mapreduce.map.cpu.vcores\
2\
mapreduce.reduce.memory.mb\
128\
mapreduce.reduce.java.opts\
-Xmx102m\
mapreduce.reduce.cpu.vcores\
2\
yarn.app.mapreduce.am.resource.mb\
128\
yarn.app.mapreduce.am.command-opts\
-Xmx102m\
yarn.app.mapreduce.am.resource.cpu-vcores\
1\
mapreduce.job.maps\
4\
mapreduce.job.reduces\
4\`\
and in `nano yarn.site.xml`\
`\
yarn.resourcemanager.resource-tracker.address\
node1:8025\
yarn.resourcemanager.scheduler.address\
node1:8035\
yarn.resourcemanager.address\
node1:8050\
yarn.nodemanager.aux-services\
mapreduce_shuffle\
yarn.nodemanager.resource.cpu-vcores\
4\
yarn.nodemanager.resource.memory-mb\
768\
yarn.scheduler.minimum-allocation-mb\
64\
yarn.scheduler.maximum-allocation-mb\
256\
yarn.scheduler.minimum-allocation-vcores\
1\
yarn.scheduler.maximum-allocation-vcores\
4\
yarn.nodemanager.vmem-check-enabled\
true\
yarn.nodemanager.pmem-check-enabled\
true\
yarn.nodemanager.vmem-pmem-ratio\
2.1\`\
To get a better performance you may experiment with some values.

#### 2.3 Install Spark

Installing Spark is easy as hell, just download and extract. Go to the opt directory, to download spark `sudo wget http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz`  (be sure to use the latest version which can be found here: <https://spark.apache.org/downloads.html>). Now extact the file with `sudo tar -xzf spark-2.1.0-bin-hadoop2.7`. To check if Spark is sucessfully installed change to `cd spark-2.1.0-bin-hadoop2.7` and run a simple example `bin/run-example SparkPi 10`.

In the next Section we will [build the cluster](https://www.thebigdatablog.com/3-build-the-cluster/).

#### REFERENCES

<http://www.becausewecangeek.com/building-a-raspberry-pi-hadoop-cluster-part-1/>