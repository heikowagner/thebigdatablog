---
categories:
- Install Spark on a OrangePi PC
- Projects
date: '2017-04-02'
slug: 4-install-scala-at-the-master-node
status: private
tags: []
title: 4. Install Scala at the Master Node
wp_id: 848
wp_modified: '2017-04-06T16:07:06'
---

### 1. Requirements

An Orangepi with Lubuntu running, see this [post](https://www.thebigdatablog.com/1-setting-up-the-orangepi/) for further instructions.

### 2.Install Scala

First Download Scala with `wget http://downloads.lightbend.com/scala/2.12.1/scala-2.12.1.tgz` (the latest version can be found [here](http://www.scala-lang.org/download/)) and extract the file to `sudo mkdir /usr/lib/scala\
sudo tar -xf scala-2.12.1.tgz -C /usr/lib/scala\
rm scala-2.12.1.tgz\`. Next create symbolic links `\
sudo ln -s /usr/lib/scala/scala-2.11.6/bin/scala /bin/scala\
sudo ln -s /usr/lib/scala/scala-2.11.6/bin/scalac /bin/scalac\`. To check if every things works run `scala -version`.