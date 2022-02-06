FROM            python:3.10 as build
MAINTAINER      Jelle Smet
COPY            . /src
WORKDIR         src
RUN             python3 -m venv /xpectd
RUN             . /xpectd/bin/activate && python3 -m ensurepip --upgrade && python3 setup.py install

FROM            python:3.10 as final
COPY            --from=build /xpectd /xpectd
EXPOSE          8080
ENTRYPOINT      ["/xpectd/bin/xpectd"]
