import datetime

def generate_template(title:str, today:datetime.date) -> str:
    template = f"""---
title: {title}
date: {today}
categories: [category1, category2]
tags: [tag1, tag2]
---
    
Write your content here.
"""
    return template


title = "Generator expression and Next() in Python"
today = datetime.date.today()
template = generate_template(title, today)

# Create a new file with the template
file_name = f"{today}-{title}.md".replace(" ", "_").lower()
with open(file_name, "w") as file:
    file.write(template)

print(f"File created: {file_name}\n")
print("ℹ️   FOR MORE INFORMATION, visit: https://chirpy.cotes.page/posts/write-a-new-post/")

print("or")
print("https://github.com/cotes2020/jekyll-theme-chirpy/blob/master/_posts/2019-08-08-write-a-new-post.md")