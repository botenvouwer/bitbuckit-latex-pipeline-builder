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

# make directories
RUN mkdir /lib/latex-builder

# Install latex builder that will do the latex building
COPY latex-builder/. /lib/latex-builder

RUN echo "export PATH=/lib/latex-builder:\$PATH" >> $HOME/.bashrc

RUN  chmod -R 777 /lib/latex-builder

