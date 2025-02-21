#!/bin/bash
echo $HOME

# Update
sudo yum update -y

# Installing uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installing git
sudo yum install git -y

# Cloning repository
git clone https://github.com/Estrategia-e-innovacion-de-TI/curso_arquitectura_informacion_MR.git

# Installing python3 and requirements
cd curso_arquitectura_informacion_MR/ms_notificaciones/
uv sync
source .venv/bin/activate
