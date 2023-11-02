FROM alvimpaulo/naoqi-python-sdk:2.8.5

# Set a directory for the app
WORKDIR /usr/src/app

# Copy all the files to the container
COPY . .

# Install necessary packages. If the naoqi library is included in the SDK image, you might not need to install it again.
RUN pip install flask paramiko numpy requests