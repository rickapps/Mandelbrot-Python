# Administer Mandelbrot plot form
from flask import Flask, render_template, request
from mandelbrot import Mandelbrot

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def plotView():
    # A post request means we are enlarging an area of the
    # previous plot.
    if request.method == 'POST':
        xc = request.form.get("xc", type=float)
        yc = request.form.get("yc", type=float)
        domain = request.form.get("xDomain", type=float)
        # Initialize our plot object
        plot = Mandelbrot(xc, yc, domain)

        xcorner = request.form.get("xtopLeft", type=float)
        ycorner = request.form.get("ytopLeft", type=float)
        xcenter = request.form.get("xcenter", type=float)
        ycenter = request.form.get("ycenter", type=float)
        # Zoom in on the area the user requested
        plot.zoom(xcorner, ycorner, xcenter, ycenter)
        thePlot = plot.makeImage()
        xc = plot.xc
        yc = plot.yc
        domain = plot.domain
    else:  
        # Display the default plot
        #plot = Mandelbrot(-0.65, 0.0, 3.4)
        # To make the initial display faster, we will just
        # load an image.
        xc = -0.65
        yc = 0.0
        domain = 3.4
        thePlot = 'static/img/mandelbrot.png'

    # Display our image and store values for the next plot
    return render_template("index.html", 
        xc=xc,
        yc=yc,
        xDomain=domain,
        image=thePlot)

@app.route("/<int:n>", methods=["GET"])
def plotSaved():
    pass

if __name__ == "__main__":
    app.run()
