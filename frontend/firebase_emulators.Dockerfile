FROM node:14.5

# Install OpenJDK-11
RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' | tee /etc/apt/sources.list.d/stretch-backports.list

RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;
RUN npm i -g firebase-tools
RUN firebase --version
EXPOSE  9099 3001