---
title: Katex and Mermaid
date: 2024-03-23 21:00:00 +0100
categories: [blog,subcategory]
tags: [testtag]     # TAG names should always be lowercase
math: true # Needed for latex, don't include by default since makes rendering a bit slower
mermaid: true # Needed for mermaid, don't include by default since make rendering a bit slower
---
## KaTeX
You can render LaTeX mathematical expressions using KaTeX:

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is written with   `$\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$`

The Euler integral:

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

is written with:

```latex
$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$
```


> You can find more information about **LaTeX** mathematical expressions [here](https://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference).

## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.
Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.
Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.
                                                                                                                                                                                                                   
Bob-->Alice: Checking with John...                                                                                                                                                                                 
Alice->John: Yes... John, how are you?                                                                                                                                                                             
```                                                                                                                                                                                                                
                                                                                                                                                                                                                   
And this will produce a flow chart:                                                                                                                                                                                
                                                                                                                                                                                                                   
```mermaid                                                                                                                                                                                                         
graph LR                                                                                                                                                                                                           
A[Square Rect] -- Link text --> B((Circle))                                                                                                                                                                        
A --> C(Round Rect)                                                                                                                                                                                                
B --> D{Rhombus}                                                                                                                                                                                                   
C --> D                                                                                                                                                                                                            
```
