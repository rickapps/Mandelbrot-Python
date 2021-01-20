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
    else:  
        # Display the default plot
        plot = Mandelbrot(-0.65, 0.0, 3.4)

    # Save our values to use on our next plot
    thePlot = plot.makeImage()
    return render_template("index.html", 
        xc=plot.xc,
        yc=plot.yc,
        xDomain=plot.domain,
        image=thePlot)

@app.route("/<int:n>", methods=["GET"])
def plotSaved():
    pass

if __name__ == "__main__":
    app.run()
