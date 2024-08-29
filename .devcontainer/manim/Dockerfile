FROM manimcommunity/manim

RUN python -m pip install manim-slides[manim]
USER root
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.56/quarto-1.5.56-linux-amd64.deb
RUN apt-get install sudo
RUN dpkg -i quarto-1.5.56-linux-amd64.deb
USER ${NB_USER}