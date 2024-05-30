---
title: CICD with GitLab
date: 2024-05-30
categories: [programming, ci/cd, gitlab]
tags: [ci/cd, gitlab, devops, programming, automation]
---
    
CI/CD (Continuous Integration/Continuous Deployment) is a practice used to automate the integration of code changes and the deployment of code to production. In larger projects it is common to have separate CI and CD pipelines, since the deployment must be handled more cautiously. The CI pipeline is then used to build and test the code, while the CD pipeline is used to deploy the code to production.

In this post we will use GitLab CI to illustrate how to set up a CI/CD pipeline. Actually we will set up two pipelines; one that triggers when code is merged and one that triggers on a schedule.

We'll assume we already have a GitLab repository set up.

## Setting up the CI pipeline
A pipeline is a set of automated tasks that are run in a specific order. In GitLab, a pipeline is defined in a file called `.gitlab-ci.yml`. This file should be placed in the root of the repository. It's kind of the backbone of the CI/CD process. A pipeline consists of stages, jobs and tasks.

## Stages
A stage is a group of jobs. The stages are defined in the `.gitlab-ci.yml` file. That 
Jobs in the same stage are run in parallel, while jobs in different stages are run sequentially. The fact that jobs in different stages are run sequentially (i.e. no job in the next stage is started until all jobs in the previous stage have finished) is a key feature of the CI/CD pipeline. You might build the code in one stage, run tests in the next stage, (possibly run more tests that depends on the results from the previous  stage in yet another stage) and deploy the code in the last stage.

Example of stages:
```yaml
stages:
- build
- test
- deploy

build_job:
  stage: build
  script:
    - echo "Building the application..."
  only:
    - main # only run this job when code is merged to the main branch

test_job:
  stage: test
  script:
    - echo "Running tests..."
  only:
    - main

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production..."
  environment: production
  only:
    - main

```

## Jobs
A job is a set of task executed as part of a stage. If a job fails, the pipeline will stop and the failed job will be marked as failed (unless specified otherwise).

In the example above we didn't really specify any tasks, we just printed some text. In a real world scenario we would probably build the code, run tests and deploy the code. The test stage could look like this where we have a shell script that runs the tests: 
```yaml
...
test_job:
  stage: test
  script:
    - echo "Running tests..." # optional
    - ./run_linters.sh # test for code quality
    - ./run_tests.sh
  only:
    - main
```
In the example above we have two tasks, `run_linters.sh` and `run_tests.sh`. They are run in sequence. If we want to run them in parallel we can use the `&` operator:
```yaml
test_job:
  stage: test
  script:
    - echo "Running tests..." # optional
    - ./run_linters.sh & ./run_tests.sh
  only:
    - main
```
<br>

If we want to run the tasks in sequence, but still continue to the next task even if the first task fails, we can use the `||` operator:
```yaml
test_job:
  stage: test
  script:
    - echo "Running tests..." # optional
    - ./run_linters.sh || true
    - ./run_tests.sh
  only:
    - main
```
<br>

If we want to run two python scripts in parallel we can do like this:
```yaml
test_job:
  stage: test
  script:
    - echo "Running tests..." # optional
    - python script1.py & python script2.py
  only:
    - main
```

## Multiple Pipelines
Let's say we want to have two pipelines; one that triggers when code is merged and one that triggers on a schedule. We have two options in GitLab CI;
1. Use the `rules` keyword  
2. Make a separate `<pipleline_name>.gitlab-ci.yml` files and specify the pipeline names in the `.gitlab-ci.yml` file.

### Using the `rules` keyword
```yaml
stages:
  - build
  - test
  - deploy

commit_build:
  stage: build
  script:
    - echo "Building the application on commit..."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'

nightly_build:
  stage: build
  script:
    - echo "Building the application nightly..."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'

commit_test:
  stage: test
  script:
    - echo "Testing the application on commit..."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'

nightly_test:
  stage: test
  script:
    - echo "Testing the application nightly..."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
```

### Using separate `<pipeline_name>.gitlab-ci.yml` files
Let's say we have two files, `commit_pipeline.gitlab-ci.yml` and `nightly_pipeline.gitlab-ci.yml` where we define the pipelines.

In the `.gitlab-ci.yml` file:
```yaml

include:
  - local: '/path/to/commit_pipeline.gitlab-ci.yml'
    rules:
      - if: '$CI_PIPELINE_SOURCE == "push"'
  - local: '/path/to/nightly_pipeline.gitlab-ci.yml'
    rules:
      - if: '$CI_PIPELINE_SOURCE == "schedule"'
```

The schedule is set in the sidebar under the Pipelines section in GitLab.

## Building and deploying a Docker container 
A common use case is to build a Docker container and deploy it to a container registry. Here is an example of how it could look to build a Docker container and deploy it to the GitLab container registry:
```yaml
stages:
  - build

variables:
  build_number: "${CI_PIPELINE_ID}-${CI_COMMIT_SHORT_SHA}"
  project_name: "your_project_name"


build_container:
    stage: build
    before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY # login to the GitLab container registry in order to push the image
    script:
        - docker build ./path/to/dockerfile -t $project_name:$build_number
        - docker push $project_name:$build_number
    only:
        - main

```

## Common tools and services
There are many tools and services that can be used in a CI/CD pipeline. Azure DevOps and GitHub Action are two other popular services.

A company might have their own git server, container registry, artifact repository etc. Then common tools for handling CI/CD workflows are Zuul(primary for project gating - don't merge bad code), GoCD (for complex pipelines) and Jenkins (for complex pipelines).