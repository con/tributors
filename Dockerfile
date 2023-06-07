FROM node:20
# docker build -t tributors .

ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8
ENV ORCID_TOKEN disabled

# Install global and local dependencies first so they can be cached.
RUN npm install -gf yarn@^1.21.1
RUN /bin/bash -c "apt-get update && apt-get install -y wget bzip2 ca-certificates git && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh"
WORKDIR /code
COPY . /code
RUN pip install . && \
    yarn add --dev all-contributors-cli && \
    git config --global user.name "github-actions" && \
    git config --global user.email "github-actions@users.noreply.github.com"

ENV PATH=$PATH:/code/node_modules/all-contributors-cli/dist
WORKDIR /github/workspace
ENTRYPOINT ["/code/docker/entrypoint.sh"]
