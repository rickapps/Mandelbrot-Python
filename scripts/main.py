# Flask route
# Generate Mandelbrot set. Return it as a string that can be 
# passed to an html img tag
#     Copyright (C) 2021  Rick Eichhorn: rickapps@live.com

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
from flask import Flask, render_template, request, session, redirect, url_for
from mandelbrot import Mandelbrot

app = Flask(__name__)
app.secret_key = 'MaNdElBrOtPlOt'
_defaultImage = '/static/img/mandelbrot.png'

def manageSession(page, xc, yc, domain):
    # Populate our session dictionary
    session['page'] = page
    if page == 0:
        session['xc'] = [xc]
        session['yc'] = [yc]
        session['domain'] = [domain]
    else:
        # Delete everything past the current page
        if page < len(session['xc']):
            session['xc'] = [session['xc'][i] for i in range(page)]
            session['yc'] = [session['yc'][i] for i in range(page)]
            session['domain'] = [session['domain'][i] for i in range(page)]
        session['xc'].append(xc)
        session['yc'].append(yc)
        session['domain'].append(domain) 

@app.route("/", methods=["POST","GET"])
def plotView():
    # A post request means we are enlarging an area of the
    # previous plot.
    if request.method == 'POST':
        # Initialize our plot object
        xc = request.form.get("xc", type=float)
        yc = request.form.get("yc", type=float)
        domain = request.form.get("xDomain", type=float)
        plot = Mandelbrot(xc, yc, domain)

        # Zoom in on the plot area requested
        xcorner = request.form.get("xtopLeft", type=float)
        ycorner = request.form.get("ytopLeft", type=float)
        xcenter = request.form.get("xcenter", type=float)
        ycenter = request.form.get("ycenter", type=float)
        plot.zoom(xcorner, ycorner, xcenter, ycenter)

        # Create our image and store the params used to make it
        thePlot = plot.makeImage()
        xc = plot.xc
        yc = plot.yc
        domain = plot.domain
        page = session['page'] + 1
        manageSession(page, xc, yc, domain)
    else:
        # Display the default plot
        page = 0
        xc = -0.65
        yc = 0.0
        domain = 3.4
        #plot = Mandelbrot(xc, yc, domain)
        # To make the initial display faster, we will just
        # load an image.
        thePlot = _defaultImage
        # Store our session
        manageSession(page, xc, yc, domain)

    # Display our image and pass values for the next plot
    return render_template("index.html", 
        xc=xc,
        yc=yc,
        xDomain=domain,
        image=thePlot)

@app.route("/page/<int:num>", methods=["GET"])
def plotSaved(num=0):
    # Use our sesssion variables to retrieve a previous plot
    if num >= 0 and num < len(session['xc']):
        # Update our page number and retrieve params
        session['page'] = num
        xc = session['xc'][num]
        yc = session['yc'][num]
        domain = session['domain'][num]

        # Initialize our plot object
        if num > 0:
            plot = Mandelbrot(xc, yc, domain)
            thePlot = plot.makeImage()
        else:
            thePlot = _defaultImage

        # Display our image and store values for the next plot
        return render_template("index.html", 
            xc=xc,
            yc=yc,
            xDomain=domain,
            image=thePlot)
    else:
            return redirect(url_for('plotView'))

if __name__ == "__main__":
    app.run()
