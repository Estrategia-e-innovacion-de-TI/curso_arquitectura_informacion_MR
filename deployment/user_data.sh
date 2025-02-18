#!/bin/bash
echo $HOME

# Install Java 11
sudo apt install openjdk-11-jre-headless -y
sudo apt install openjdk-11-jdk-headless -y

# Download jmeter
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip

# Unzip jmeter
unzip apache-jmeter-5.6.3.zip -d /opt/jmeter-5.6.3

# Add jmeter to PATH
echo "export PATH=$PATH:/opt/jmeter-5.6.3/apache-jmeter-5.6.3/bin" >> ~/.bashrc
source ~/.bashrc