FROM node:12
# docker build -t allcontributors .

# Set up working directory.
RUN mkdir -p /code
WORKDIR /code

# Install global and local dependencies first so they can be cached.
RUN npm install -gf yarn@^1.21.1 && \
    apt-get update && \ 
    apt-get install -y python3-pip
COPY . /code
RUN mv /code/a2z.py /usr/local/bin/a2z && \
    pip3 install -r /code/requirements.txt && \
    yarn add --dev all-contributors-cli && \
    git config --global user.name "github-actions" && \
    git config --global user.email "github-actions@users.noreply.github.com"

ENV PATH=$PATH:/code/node_modules/all-contributors-cli/dist
WORKDIR /github/workspace
ENTRYPOINT ["/code/entrypoint.sh"]
