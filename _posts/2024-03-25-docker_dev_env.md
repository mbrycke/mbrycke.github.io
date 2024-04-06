---
title: Docker Development Environment
date: 2024-03-25
categories: [docker, development]
tags: [docker, docker-compose, ssh, vscode,  openssh-server, ubuntu, postgres]
---
    
# Create a docker development environment
It can be a good idea to create a docker development container. In this way you can install all the tools you need, remove them, and start over again without messing up your host system.

## Intro
The idea is to create a docker container with all the tools you need for development and connect to it with ssh. This way you can e.g. use vscode on your host system to connect to the container using the remote ssh extension. This will be like developing on a remote server, but the server is your own computer.

## 1. Creating Dockerfile

To create the container, you can use the following Dockerfile:

```Dockerfile
FROM ubuntu:22.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        gnupg2 \
        lsb-release \
        wget \
        sudo \
        neovim \
    && rm -rf /var/lib/apt/lists/*

# Install Python3 and pip
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Install Bazel
RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel-archive-keyring.gpg \
    && mv bazel-archive-keyring.gpg /usr/share/keyrings \
    && echo "deb [signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends bazel \
    && rm -rf /var/lib/apt/lists/*


# Install SSH server
RUN apt-get update && apt-get install -y openssh-server

# Set up SSH daemon
RUN mkdir /var/run/sshd

# Add user for SSH (Change 'your_user' and 'your_password' to your desired credentials)
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 ubuntu
RUN  echo 'ubuntu:password' | chpasswd

# SSH login fix. Otherwise user is kicked off after login
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Change the SSH port if desired (Optional)
# RUN echo "Port 2222" >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Set up workspace directory
WORKDIR /workspace
```
## 2. Build the image

```bash
docker build -t ubuntu-dev .
```
This will build the image from the Dockerfile and name it `ubuntu-dev`. The `.` at the end of the command means that it will look for the Dockerfile in the current directory. Therefore you should run this command in the same directory as the Dockerfile.

## 3. Run the container, use the command:

```bash
docker run -d -p 2222:22 --name dev-env ubuntu-dev
```
This will build the container from the Dockerfile and name it `dev-env`. The container will be accessible on port 2222. It will use the image `ubuntu-dev`.

`-d` means that the container will run in detached mode, i.e. in the background.

## 3. Connect to the container
You can connect to the container using ssh. The user is `ubuntu` and the password is `password`. You can connect to the container using the command:

```bash
ssh ubuntu@localhost -p 2222
```
To be able to connect with just `ssh localhost` you can add the following to your `~/.ssh/config` file:

```bash
Host dev-env
    HostName localhost
    Port 2222
    User ubuntu
```

## 4. Add hosts public key to authorized keys
To be able to connect to the container without a password, you can add your host's public key to the container's authorized keys. You can do this by running the following command on your host system:
### create .ssh
```bash
ssh ubuntu@localhost -p 2222 'mkdir .ssh'
```

### add public key to authorized keys
```bash
cat ~/.ssh/id_rsa.pub | ssh ubuntu@localhost -p 2222 'cat >> .ssh/authorized_keys'
```
## 5. Connect to the container using vscode
Install the remote ssh extension in vscode. Then you can connect to the container by pressing ctrl+shift+p and typing `Remote-SSH: Connect to Host...`. Then type `ssh dev-env` and you will be connected to the container.


## 6. Persisting data
In order to persist data even if the container is deleted, you can use a persistent volume. This is a directory on the host system that is mounted into the container. This way the data is stored on the host system and not in the container.

To create a persistent volume, you can use the `docker volume create` command.

```bash

docker volume create dev_container_data 
```

Stop the container and remove it in order to run with a volume instead.
```bash
docker stop dev-env

docker rm dev-env
```

Then attach the volume to a container using the `-v` flag.

```bash
docker run -d -p 2222:22 --name dev-env ubuntu-dev -v dev_container_data:/path/in/container
```

Now all data written to `/path/in/container` will be stored on the host system in the directory `dev_container_data`. Instead of `dev_container_data` you can use a path to a directory on your host system.

## 7. User docker compose
We might want to use other services like a postgres database or a redis server in our development environment. We can use docker compose to start all these services at once. Create a file called `docker-compose.yml` with the following content:

### you can skip step 2, 3 and 6 if you use docker compose
since docker compose will build the image for you and you can specify the volume in the docker-compose file.


```yaml
version: '3.8'

services:
  dev_container:
    build: .
    depends_on:
      - db
    ports:
      - 2222:22 # This exposes the container's SSH server on port 2222
    restart: unless-stopped # Restart the container unless it was stopped by the user
    volumes:
      - dev_container_data:/home/ubuntu # Creates a volume for the container's /app directory. I.e files in the container's /app directory will be stored on the host machine in the volume dev_container_data. You can specify a path on the host machine to store the volume by changing the left side of the colon. E.g. /path/on/host:/home/ubuntu. Note that it is not recomended (or even possible?) to mount the root directory of the docker container to the host machine.
      - /home/myhome/data/data:/home/ubuntu/data # mounts a directory on the host machine to a directory in the container. In this case /home/myhome/data/data on the host machine is mounted to /home/ubuntu/data in the container. This is useful if you want to share/store data on the host machine.

  db:
    image: postgres:latest
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: postgres_db 
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    restart: unless-stopped
    ports:
      - 5432:5432 # This exposes the container's PostgreSQL server on port 5432 for the host machine to connect to. The dev_container does not need to connect to the database through this exposed port as it can connect to the database through the container's network. The host machine can connect on 127.0.0.1:5432 (or localhost:5432)

volumes:
  dev_container_data:
  db-data:
```

Then you can start the services with the command:

```bash
docker compose up -d
```

Stop the services with the command:

```bash
docker compose down
```

If you make changes to the Dockerfile or the docker-compose.yml file, you can rebuild the image with the command:

```bash
docker compose up -d --build
```

# Access the host system's GPU (NVIDIA)
To be able to access the host system's GPU from the container you need 2 things.

1. Install the NVIDIA Container Toolkit. You can do this by following the instructions on the [NVIDIA Container Toolkit GitHub page](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

2. Start the container with the `--gpus all` (or specify which GPU) flag. This will give the container access to all the host system's GPUs. **Or, since we are using docker-compose, you can add the following to the** `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  dev_container:
    build: .
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    depends_on:
    ...
```
You need to rebuild the image with `docker compose up -d --build` after adding this to the `docker-compose.yml` file.




