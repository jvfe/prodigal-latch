FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

RUN apt-get install -y curl

# Install Prodigal
RUN curl -L https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux -o prodigal &&\
    chmod +x prodigal

COPY data /root/

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
