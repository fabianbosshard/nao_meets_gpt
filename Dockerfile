# Using Ubuntu 17.04 as specified by the NAOqi docs
FROM python:2.7.8-wheezy

# Install pip
#RUN apt-get update && apt-get install -y python2 alsa-base alsa-utils wget

RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py

# Set the working directory to /naoqi
#WORKDIR /naoqi

# Copy the NAOqi for Python SDK
#ADD pynaoqi-python2.7-2.1.4.13-linux64.tar.gz /naoqi/

# Copy the boost fix
# Kudos https://community.ald.softbankrobotics.com/en/forum/import-issue-pynaoqi-214-ubuntu-7956
#ADD boost/* /naoqi/pynaoqi-python2.7-2.1.4.13-linux64/

# Set the path to the SDK
ENV PYTHONPATH=${PYTHONPATH}:/nao/devtools/pynaoqi-python2.7-2.8.5.10-linux64/lib/python2.7/site-packages
#ENV LD_LIBRARY_PATH="/nao/devtools/pynaoqi-python2.7-2.8.5.10-linux64:$LD_LIBRARY_PATH"

ENV QI_SDK_PREFIX=/nao/devtools/pynaoqi-python2.7-2.8.5.10-linux64

# Set a directory for the app
WORKDIR /usr/src/app

# Copy all the files to the container
COPY . .

# Install necessary packages. If the naoqi library is included in the SDK image, you might not need to install it again.
RUN pip install flask paramiko numpy requests

# expose the port
EXPOSE 5004

ENTRYPOINT [ "tail", "-f", "/dev/null" ]