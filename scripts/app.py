# Administer Mandelbrot plot form
from flask import Flask, render_template, request
from mandelbrot import Mandelbrot

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def plotView():
    # A post request means we are enlarging an area of the
    # previous plot.
    if request.method == 'POST':
        plot = Mandelbrot(-0.65, 0.0, 3.4)
        pngImageB64String = plot.makeImage() 
    else:  
        # Display the default plot
        plot = Mandelbrot(-0.65, 0.0, 3.4)
        pngImageB64String = plot.makeImage() 

    return render_template("index.html", image=pngImageB64String)

@app.route("/<int:n>", methods=["GET"])
def plotSaved():
    pass

if __name__ == "__main__":
    app.run()
