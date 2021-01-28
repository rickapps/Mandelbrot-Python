# Mandelbrot-Python
Practice project for learning Flask, Jupyter Lab

A website that displays a mandelbrot set and allows you to continually magnify sections of the plot to see the endless border detail. View website here:
[Mandelbrot Set](https://rickapps.pythonanywhere.com). Although many images are generated by the site, none are written to disk. Instead, images are encoded as byte strings and set to the src property of the img tag. The tool to select portions of the image is implemented using jqueryui draggable. 

![screenshot of plot](scripts/static/img/screenshot.png "Mandelbrot Set").

The idea came from reading this article on Medium: [Visualizing the Mandelbrot Set](https://medium.com/swlh/visualizing-the-mandelbrot-set-using-python-50-lines-f6aa5a05cf0f).
The article made me curious so I researched Mandelbrot on [+Plus Magazine](https://plus.maths.org/content). For flask coding I looked at: [Flask Tutorial](https://code-maven.com/hello-world-with-flask-and-python).

