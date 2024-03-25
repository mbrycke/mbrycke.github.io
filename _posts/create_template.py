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


title = "My New Post"
today = datetime.date.today()
template = generate_template(title, today)

# Create a new file with the template
file_name = f"{today}-{title}.md".replace(" ", "_").lower()
with open(file_name, "w") as file:
    file.write(template)

print(f"File created: {file_name}\n")
print("ℹ️   FOR MORE INFORMATION, visit: https://chirpy.cotes.page/posts/write-a-new-post/")