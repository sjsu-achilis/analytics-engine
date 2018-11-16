#!/bin/bash

# build docker image
docker build --no-cache -t achcore .

# tag with repo
docker tag achcore:latest pankajchandan/achcore:latest

# do docker login here if pushing to remote registry
docker login

# push here
docker push pankajchandan/achcore:latest
