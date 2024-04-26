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

How to best split the data is not a trivial matter. The most straightforward way is to split the data into chunks of a few sentences each. But after a some thought we soon realize that there are lots of things to factor. To small chunks will give lots of chunks with similar data - and perhaps we will loose some context. To big chunks will require us to have a huge context window when we query the model. And also, depending on the model we use for embeddings, the model might not be able to handle very long texts efficiently. Preferably we would also like to have chunks that are split on the basis of the content of the text. Depeding on how we split we might also want som overlap between the chunks. Etc.

We will settle for a fairly simple method since this is more about outlining the principles and not aiming for optimal performance.

