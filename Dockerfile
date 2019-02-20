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

#install python -> we need this to run the build script
RUN apt-get install -y python3 python3-pip

RUN pip3 install gitpython

# make directories
#RUN mkdir /lib/latex-builder

RUN mkdir /lib/tag_rund
RUN mkdir /home/test-tex-file

#Depricated
# Install latex builder that will do the latex building
#COPY latex-builder/. /lib/latex-builder

COPY tag_rund/. /lib/tag_rund
COPY test-tex-file/. /home/test-tex-file

#RUN echo "export PATH=/lib/latex-builder:\$PATH" >> $HOME/.bashrc

RUN echo "export PATH=/lib/tag_rund:\$PATH" >> $HOME/.bashrc

#RUN  chmod -R 777 /lib/latex-builder

RUN  chmod -R 777 /lib/tag_rund

RUN git config --global user.email "noreplay@robot.com" && git config --global user.name "Robot"

#Temp for testing -> staticly log in for git
#COPY credentials /root/.netrc

#Temp for testing -> get the git repo for code run
#RUN cd /home
#RUN git clone https://bitbucket.org/botenvouwer/pipelinetest.git
