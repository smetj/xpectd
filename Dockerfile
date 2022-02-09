FROM            pypy:3.8-7-slim as build
MAINTAINER      Jelle Smet
COPY            . /src
WORKDIR         src
RUN             apt-get update && apt-get install -y build-essential
RUN             python3 -m venv /xpectd
RUN             . /xpectd/bin/activate && python3 -m ensurepip --upgrade && python3 setup.py install

FROM            pypy:3.8-7-slim as final
COPY            --from=build /xpectd /xpectd
EXPOSE          8080
ENTRYPOINT      ["/xpectd/bin/xpectd"]
