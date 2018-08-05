#!/bin/bash

# build docker image
docker build -t synthetic .

# tag with repo
docker tag core:latest pankajchandan/core:latest

# do docker login here if pushing to remote registry
docker login

# push here
docker push pankajchandan/core:latest
