
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8888


# Creation of the workdir
RUN mkdir -p /code/kblog

# Changes to workdir
WORKDIR /code/kblog

# Add rsource to container 
ADD src /code/kblog

# Install requirements
RUN pip install -r /code/kblog/requirements.txt

# Add entrypoint
ADD docker/docker-entrypoint.sh /code
RUN chmod +x /code/docker-entrypoint.sh
ENTRYPOINT [ "/code/docker-entrypoint.sh" ]
