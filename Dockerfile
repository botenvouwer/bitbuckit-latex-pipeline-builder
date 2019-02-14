FROM ubuntu:latest
MAINTAINER William Loosman <william.wl@live.nl>
ENV DEBIAN_FRONTEND noninteractive

# update software repository
RUN apt-get update -q

# install latex
RUN apt-get install -qy texlive-full

# remove documentation packages of latex to save disk space
RUN apt-get remove --quiet --yes "texlive-*-doc"

# install some additional tools    
RUN apt-get install -qy make latexmk git

