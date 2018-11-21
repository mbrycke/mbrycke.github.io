---
layout: post
title: Git basics
---
# Git basics

## Installation
(provided you're using the APT package manager, like the default on Debian/Ubuntu)
```ssh
$sudo apt-get install git git-extras
```
## Create a git repository
cd into the directory you wish to create a repository for. Then initialize a git-repository by
```ssh
$git init
```
Now, go to [Github](https://github.com/) and create a repository for the project. (First you need to create an account on github if you don't have it, and log in)
/images/git1.png
Click on start object and fill out the form you are linked to, i.e. Repository name, and optional Description. Then click no 'Create repository' /images/cloneordownload.png
Copy the link which show up. Go back to the terminal and and paste the link in the git command below
```ssh
$git remote add origin https://github.com/your/link.git
```
We have now told the lokal repository where its remote origin is. Note that 'origin' is just an alias for your repository name. 

## Configure repository
Configure user accout with the config command
```ssh
$git config --global user.name "youre_git_username"
$git config --global user.email adress@email.com
```

The easiest way to make your first post is to edit this one. Go into /_posts/ and update the Hello World markdown file. For more instructions head over to the [Jekyll Now repository](https://github.com/barryclark/jekyll-now) on GitHub.