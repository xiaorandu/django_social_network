# Use the Ubuntu 18.04 base image
FROM ubuntu:18.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update the system and install necessary packages
RUN apt-get update && \
    apt-get install -y vim python3 python3-pip wget dos2unix sudo lsb-release && \
    apt-get clean

# Set the root password (replace 'rootpassword' with the desired password)
RUN echo 'root:rootpassword' | chpasswd

# Create a new user with sudo privileges (replace 'username' with the desired username)
ARG USERNAME=username
RUN adduser --disabled-password --gecos '' $USERNAME && \
    echo "$USERNAME:password" | chpasswd && \
    usermod -aG sudo $USERNAME

# Set up the working directory
WORKDIR /vagrant

# Copy the provision.sh and requirements.txt files into the container
COPY provision.sh requirements.txt /vagrant/

# Convert the provision.sh and requirements.txt files to Unix format
RUN dos2unix /vagrant/provision.sh /vagrant/requirements.txt

# Make provision.sh executable and run it
RUN chmod +x /vagrant/provision.sh && /vagrant/provision.sh

# Add environment variable
RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/$USERNAME/.bashrc

# Switch to the new user
USER $USERNAME

# Set the entrypoint
ENTRYPOINT ["/bin/bash"]

# Expose any necessary ports
EXPOSE 8000
