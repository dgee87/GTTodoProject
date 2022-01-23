FROM python:3.7-slim

RUN apt-get update

RUN groupadd developers && useradd -ms /bin/bash -g developers project
USER project
WORKDIR /home/project

ENV PATH="/home/project/.local/bin:$PATH"

COPY --chown=developers:project . ./

CMD ["python", "main.py"]