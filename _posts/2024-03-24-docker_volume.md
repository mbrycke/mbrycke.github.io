---
title: Persistent Volumes in Docker
date: 2024-03-24
categories: [docker, volume]
tags: [linux, docker]
---

## Intro

Data is actually persistent in a docker container if the container is restarted on e.g. a system reboot. This is because the data is stored in the container's writable layer.

However, if the container is deleted. A container could easily be accidentally deleted, especaially when not running. A command like `docker system prune -a` will delete all stopped containers, all networks not used by at least one container, all dangling images, and all build cache.

The solution to this is to use a persistent volume. A persistent volume is a directory on the host system that is mounted into the container. This way the data is stored on the host system and not in the container. 

## Creating a persistent volume

To create a persistent volume, you can use the `docker volume create` command. 

```bash
docker volume create my_volume
```
Then attach the volume to a container using the `-v` flag.

```bash
docker run -v my_volume:/path/in/container my_image_name
```
(this will build a container from the image `my_image_name` and attach the volume `my_volume` to the container at the path `/path/in/container`)
All data written to `/path/in/container` will be stored on the host system in the directory `my_volume`.

## Listing volumes

To list all volumes on the system, use the command:

```bash
docker volume ls
```
For more information about a specific volume, use the command

```bash
docker volume inspect
```

## Removing volumes

To remove a volume, use the command:

```bash
docker volume rm my_volume
```
You can also remove unused volumes with the command:

```bash
docker volume prune
```
or include in the `docker system prune` command with the `-v` flag.


## Sharing volumes between containers

To share a volume between containers, you can use the `--volumes-from` flag.

```bash
docker run --volumes-from my_container my_image_name
```
This will create a new container from the image `my_image_name` and attach the volumes from the container `my_container`.