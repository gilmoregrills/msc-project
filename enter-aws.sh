#!/bin/bash

ssh -i "aws-keys/msc-project.pem" ubuntu@ec2-35-176-144-147.eu-west-2.compute.amazonaws.com
cd msc-project/implementation/individualiser/individualiser
python __main__.py
