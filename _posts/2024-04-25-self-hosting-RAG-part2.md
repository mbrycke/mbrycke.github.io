---
title: Self-hosting RAG part2
date: 2024-04-25
categories: [deep learning,rag]
tags: [vector database, embeddings, rag, self-hosting, docker, postgresql, pgvector]
---
    
## Introduction
In the previous post we set up a server for the embeddings model. In this part we will populate the database with the data and the embeddings.

## Splitting the data into chunks
The idea is to split the data into chunks and store the chunks in the database. We will also store the embeddings of the chunks in the database.