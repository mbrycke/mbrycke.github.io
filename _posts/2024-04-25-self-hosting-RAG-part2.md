---
title: Self-hosting RAG part2
date: 2024-04-25
categories: [deep learning,rag]
tags: [vector database, embeddings, rag, self-hosting, postgresql, pgvector]
---
    
## Introduction
In the previous post we set up a server for the embeddings model. In this part we will populate the database with the data and the embeddings.

## Splitting the data into chunks
The idea is to split the data into chunks and store the chunks in the database. We will also store the embeddings of the chunks in the database.

How to best split the data is not a trivial matter. The most straightforward way is to split the data into chunks of a few sentences each. But after a some thought we soon realize that there are lots of things to factor. To small chunks will give lots of chunks with similar data - and perhaps we will loose some context. To big chunks will require us to have a huge context window when we query the model. And also, depending on the model we use for embeddings, the model might not be able to handle very long texts efficiently. Preferably we would also like to have chunks that are split on the basis of the content of the text. Depeding on how we split we might also want som overlap between the chunks. Etc.

Howeever, in practice we can get pretty far by just splitting the data into chunks of size of typically about 512-1024 token. If we don't have any semantical analysis of the text we can compensate by having some overlap between the chunks.

There are so many parameters to consider that it's probably best to just try out different things and see what works best for your data and your model.

I've tried splitting text into chunks with semantical analysis using mistral:7b and mixtra:8x7b. A very easy way is to just ask mixtral:8x7b (mistral:7b will tends to alter the text using this method) to split the text into paragraphs with similar content and then bundel them into suitable chunks. This is quite time consuming and might not be worth the effort - again depending on the context.

## Populating the database
Now that we have the data split into chunks we need to create embeddings of the chunks and store the data and the embeddings in the database. At the time of writing probably among the best embeddings model is one of OpenAI's models. `text-embedding-3-small` gives costs 1 dollar for about `62,500` worth of pages which is quite cheap. However, you then you also need to use the OpenAI API everytime you want to search the database. And we want to self host. We saw an example of hos to self host a model in part 1. Now that we have embeddings we can store them in our postgres database(with the pgvector extension). First create a table that can store 4096 elements (the number of elements in our embedding vector).

```sql
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    vector_data vector(4096)
);
```

We can then store data in the table like this:

```sql
INSERT INTO embeddings (content, vector_data) VALUES ('This is a test', '{0.219.., 0.193...}');
```

And then we can query the database and retrieve the e.g. 5 most similar entires to the embeddings in a give query.

```sql
SELECT id, content FROM embeddings ORDER BY vector_data <-> '{0.219.., 0.193...}' LIMIT 5;
```

Now we can use the retrieved data, feed it to a generative language model and ask the model to generate the most relevant information to the query.

*This was quite a handwavy explanation of how to generate embeddings, store and retrieve them. I might add more details later.*


