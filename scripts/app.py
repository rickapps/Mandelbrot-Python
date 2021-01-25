# Administer Mandelbrot plot form
from flask import Flask, render_template, request, session
from mandelbrot import Mandelbrot

app = Flask(__name__)
app.secret_key = 'MaNdElBrOtPlOt'

@app.route("/", methods=["POST","GET"])
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
        page = session['page'] + 1
        # Delete everything past the current page
        if page < len(session['xc']):
            session['xc'] = [session['xc'][i] for i in range(page)]
            session['yc'] = [session['yc'][i] for i in range(page)]
            session['domain'] = [session['domain'][i] for i in range(page)]
        session['page'] = page
        session['xc'].append(xc)
        session['yc'].append(yc)
        session['domain'].append(domain)    
    else:
        # Display the default plot
        #plot = Mandelbrot(-0.65, 0.0, 3.4)
        # To make the initial display faster, we will just
        # load an image.
        xc = -0.65
        yc = 0.0
        domain = 3.4
        thePlot = 'static/img/mandelbrot.png'
        session['page'] = 0
        session['xc'] = [-0.65]
        session['yc'] = [0.0]
        session['domain'] = [3.4]    
    # Display our image and store values for the next plot
    return render_template("index.html", 
        xc=xc,
        yc=yc,
        xDomain=domain,
        image=thePlot)

@app.route("/page/<int:num>", methods=["GET"])
def plotSaved(num=0):
    # Use our sesssion variables to retrieve a previous plot
    if num < len(session['xc']):
        xc = session['xc'][num]
        yc = session['yc'][num]
        domain = session['domain'][num]
        plot = Mandelbrot(xc, yc, domain)
        thePlot = plot.makeImage()
        session['page'] = num
        # Display our image and store values for the next plot
        return render_template("index.html", 
            xc=xc,
            yc=yc,
            xDomain=domain,
            image=thePlot)

if __name__ == "__main__":
    app.run()
