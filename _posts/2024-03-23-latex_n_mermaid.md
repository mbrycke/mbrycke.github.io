---
title: Katex and Mermaid
date: 2024-03-23 21:00:00 +0100
categories: [blog,sub_category]
tags: [test_tag]     # TAG names should always be lowercase
---
## KaTeX
You can render LaTeX mathematical expressions using KaTeX:

The Gamma function satisfying Γ(n) = (n-1)! ∀ n∈\mathbb N is via the Euler integral

$$
Γ(z) = \int₀^∞ tᶻ⁻¹e⁻ᵗdt\,.
$$


> You can find more information about LaTeX mathematical expressions here.

## UML diagrams

You can render UML diagrams using Mermaid. For example, this will produce a sequence diagram:

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
