---
title: How does Docker work?
date: 2024-06-18
categories: [docker, devops]
tags: [docker, devops]

---
    
The reason docker is more lightweight than a virtual machine is that it doesn't run a full operating system. Instead, it shares the host operating system kernel. This is why you cannot run a Windows container on a Linux host (not for real at least, there are workarounds that 'appears' to run windows in a container).

## File system isolation and layered architecture
Docker containers are built on a layered architecture. This means that a container is built on top of an image. An image is a read-only template with instructions for creating a container. An image can be built from a Dockerfile, containing the instructions for creating the image. An image can be based on another image. This is common and you see this in the `Dockerfile` with the `FROM` instruction.

The file system of a container is isolated from the host system. This is done by using a copy-on-write file system. When a container is started, a new layer is added on top of the image. This layer is read-only and the container can only write to this layer. This is why changes to the file system in a container is lost when the container is removed. You can however mount a volume to a container to persist data, i.e. write to the host file system. And you can also mount directories/disks from the host to the container to share data between the host and the container.

You can say in a slightly handwavey way that a container creates a new file system, i.e. creates a root directory, and then mounts the image on top of this root directory. This is why you can see the file system of a container by running `docker exec -it container_name /bin/bash` and then `ls /`.

## Network isolation
A container has its own network stack. This means that a container can have its own IP address, its own network interfaces, and its own routing table. This is why you can run multiple containers on the same host and they can communicate with each other without interfering with each other. You can also expose ports from the container to the host, i.e. map a port from the container to a port on the host. This is done by using the `-p` flag when running a container, e.g. `docker run -p 8080:80 my_image`.

## Benefits of Docker
There are perhaps 3 main benefits of using Docker:
- Portability: You can run the same container on different hosts, i.e. you can run the same container on your local machine, on a server in the cloud, etc.
- Isoaltion: Containers are isolated from each other and from the host system. (not counting bind mounts of volumes) 
- Resource efficiency: Containers are lightweight and share the host operating system kernel. Therefore it's much more lightweight than a virtual machine.

