---
categories:
- All Articles
- Hardware
- Install Spark on a OrangePi PC
- Projects
date: '2017-02-11'
slug: 1-setting-up-the-orangepi
status: publish
tags: []
title: 1. Setting up the OrangePi
wp_id: 421
wp_modified: '2023-10-01T10:13:10'
---

### 1. Requirements

- OrangePI PC
- SD Card (larger than 8GB)
- 4.0\*1.7 Powersuppy or USB Cable and Charger (min. 2A)
- WLAN Adapter or Ethernet Cable
- HDMI Cable and Monitor (only for setup)

### 2. Preliminary Notes

[![](http://www.add-ons.de/thebigdatablog/wp-content/uploads/2016/12/DSC0820-300x200.jpg)](http://www.add-ons.de/thebigdatablog/wp-content/uploads/2016/12/DSC0820.jpg)

OrangePi PC powered using the GPIO with USB Wlan Adapter and HDMI.

One topic of this Blog is to carry out different project to get the reader in touch with an big data enviroment. I therefore decided to buils a small cluster that run these projects based on OrangePis. There is no particular reason to use a OrangePi instead of a RaspberryPi . The reason for me to use an OrangePi is the price tag, the OrangePi cost half as much than the Raspberry with comparable or better performance. In my opionon the main reason to stick to the Raspberry is the great driver support by the community when it comes to projects concerning the GPIO. A spark installation in contrast does only depend on the operation system and no additional drives is needed. I also want to note, that this tutorial might also work for a Raspberry Pi 2 or 3 using Raspberrian (RaspberryPi 1 or Zero will not work since Spark needs more that 512 MB Ram).

Powering the OrangePi is an issue. For powering the OrangePi does not use a Mini-USB port but uses a 4.0\*1.7 round plug, which is simular to the PSP charger. The charger from Ebay, even though it states that the required 2A are supplied, did not work. The OrangePi does not work at all (only the red LED was illuminaed) or get stuck during the bootup process. As workaround i modified a USB cable and uses the powerlines to power the OrangePI trough the GPIO (**Pin 2 is + and Pin 6 is ground**).

### 3. Prepare the OrangePI

At first an operation System is needed to host the Spark installation. My choice here was Lubuntu which is a slim version of Ubuntu.

#### 3.1 Install Lubuntu using Windows

- Download [Lubuntu](http://www.orangepi.org/downloadresources/orangepipc/oragepipc_4a0e8d960f7f0a52606dfaba58.html) for OrangePI PC.
- Download [scriptbin\_kernel.tat.gz](https://drive.google.com/drive/folders/0B1hyW7T0dqn6fndnZTRhRm5BaW4zVDVyTGlGMWJES3Z1eXVDQzI5R1lnV21oRHFsWnVwSEU)
- Download and install [7zip](http://www.7-zip.org/) to extract the img file.
- Format the SD Card using [SD Formatter](https://www.heise.de/download/product/sd-formatter-74314).
- Write the img file to SD using [Win32 Disc Imager](https://sourceforge.net/projects/win32diskimager/).

Now replace at the partition readable with windows uImage by and script.bin by uImage\_OPI-2 (rename to uImage) by script.bin.OPI-PC\_720p60 (rename to script.bin). If powered the OrangePi should now reboot.

#### 3.2 Expanding the root Partition

No matter which kind of SD Card was chosen the size of the root partition is only approx. 4GB. From these 4GB more than 80% are in use. To install Hadoop, Spark and Rstudio we need to expand the size of the root partition.

Access the OrangePi using Keyboard and Monior due to Terminal or SSH using [PuttY](http://www.putty.org/). Login and Password are **orangepi**.

The idea now is to delete the exiting root partiton, then recreate the partiton with bigger size starting at the same sector. This is possible becuase the partition manager does not delete the data. To do so we first need to determine the start sector of the the root partition by `sudo fdisk /dev/mmcblk0` and `p` to list the existing partitions. **Note the start sector** of the second partition. Now type `p` and then `2` to delete the scond partiton. Now recreate the partition with `n`, `p` and `2`. As start sector use the previously noted start sector as end sector simply press return to assign all aviable space of the SD Card. Now `w` to write the partition tables. Now reboot the Pi with `sudo reboot`. After reboot, login again and use `sudo resize2fs /dev/mmcblk0p2`, reboot again (`sudo reboot`) and you are ready to set up the big data enviroment.

In the next Section we will [install Hadoop and Spark](https://www.thebigdatablog.com/2-installing-hadoop/).