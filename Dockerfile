FROM python:3.13-bookworm

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository contrib
RUN apt-get update && apt-get install -y git cmake ninja-build build-essential libboost-program-options-dev libboost-filesystem-dev \
    libboost-graph-dev libboost-system-dev libeigen3-dev libflann-dev libfreeimage-dev libmetis-dev \
    libgoogle-glog-dev libgtest-dev libgmock-dev libsqlite3-dev libglew-dev qtbase5-dev libqt5opengl5-dev \
    libcgal-dev libceres-dev

WORKDIR /usr/src/app
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt
COPY . .

CMD [ "python", "./main.py" ]
