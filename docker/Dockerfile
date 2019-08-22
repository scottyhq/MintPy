# use debian as base image
FROM debian:stretch-slim

# Label image
LABEL \
    "Description"="Container for open source time series InSAR processing with Mintpy" \
    "Github Source"="https://github.com/insarlab/MintPy/" \
    "Installation"="https://github.com/insarlab/MintPy/blob/master/docs/installation.md" \
    "Dockerfile Author"="Andre Theron" \
    "Email"="andretheronsa@gmail.com"

# Install useful programs - Libgeos + build essential (gcc) required for basemap mpl toolkits
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    wget \ 
    vim \
    libgeos-3.5.1 \
    libgeos-c1v5 \
    libgeos-dev \
    libgeos++-dev \
    zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Change default shell from dash to bash
RUN ln -sf bash /bin/sh

# Prepare build time environment for conda and mintpy
ARG MINTPY_HOME=/home/python/MintPy
ARG PYTHON3DIR=/home/python/miniconda3
ARG PYAPS_HOME=/home/python/PyAPS
ARG WORK_DIR=/home/work/
ARG PYTHONPATH=""

# Prepare container environment
ENV MINTPY_HOME=${MINTPY_HOME}
ENV PYTHON3DIR=${PYTHON3DIR}
ENV PYAPS_HOME=${PYAPS_HOME}
ENV PATH=${MINTPY_HOME}/mintpy:${MINTPY_HOME}/sh:${PYTHON3DIR}/bin:${PATH}
ENV PYTHONPATH=${PYTHONPATH}:${MINTPY_HOME}:${PYAPS_HOME}
ENV PROJ_LIB=${PYTHON3DIR}/share/proj

# Set workdir
WORKDIR /home/python

# Pull mintpy
RUN git clone https://github.com/insarlab/MintPy.git $MINTPY_HOME

# Pull PyAPS
RUN git clone https://github.com/yunjunz/pyaps3.git $PYAPS_HOME/pyaps3

# Install miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x ./Miniconda3-latest-Linux-x86_64.sh  && \
    ./Miniconda3-latest-Linux-x86_64.sh -b -p ${PYTHON3DIR} && \
    ${PYTHON3DIR}/bin/conda update -n base -c defaults conda && \
    rm ./Miniconda3-latest-Linux-x86_64.sh

# Install dependencies
RUN ${PYTHON3DIR}/bin/conda config --add channels conda-forge && \
    ${PYTHON3DIR}/bin/conda install --yes --file ${MINTPY_HOME}/docs/conda.txt

# Install things not on conda
RUN ${PYTHON3DIR}/bin/pip install git+https://github.com/matplotlib/basemap.git#egg=mpl_toolkits  && \
    ${PYTHON3DIR}/bin/pip install git+https://github.com/tylere/pykml.git

# Install DASK - not tested yet
RUN mkdir -p /home/.config/dask && \
    cp ${MINTPY_HOME}/mintpy/defaults/dask.yaml /home/.config/dask/dask.yaml

# Set working directory ENV - map a host data volume to this using "docker build . -t mintpy && docker run mintpy -v /host/path/to/data:/home/work/"
RUN mkdir -p ${WORK_DIR}
ENV WORK_DIR=${WORK_DIR}
WORKDIR ${WORK_DIR}

# Copy custom app scripts to app folder - not required
COPY ["./", "/home/app/"]

# Run entrypoint script - not required
CMD ["python3", "/home/app/app.py"]
