#!/bin/bash
echo $HOME

# Update
sudo apt update -y

# Install Java 11
sudo apt install openjdk-21-jre-headless -y
sudo apt install openjdk-21-jdk-headless -y

# Download jmeter
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip

# Unzip jmeter
sudo apt install unzip -y
sudo unzip apache-jmeter-5.6.3.zip -d /opt/jmeter-5.6.3

# Add jmeter to PATH
echo "export PATH=$PATH:/opt/jmeter-5.6.3/apache-jmeter-5.6.3/bin" >> ~/.bashrc
source ~/.bashrc

# clone the repository
git clone https://github.com/Estrategia-e-innovacion-de-TI/curso_arquitectura_informacion_MR.git