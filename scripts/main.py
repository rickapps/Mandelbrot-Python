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
import os
from flask import Flask, render_template, request, session, redirect, url_for
from mandelbrot import Mandelbrot

app = Flask(__name__)
app.secret_key = 'MaNdElBrOtPlOt'
_defaultImage = '/static/img/mandelbrot.png'
# Google Analytics ID. Set only on the production server so local runs
# and forks of this repo don't report to our analytics. It can come from
# the environment or from settings.cfg next to main.py (gitignored), since
# Synology Web Station regenerates its uWSGI config.
app.config.from_pyfile('settings.cfg', silent=True)
_gaId = os.environ.get('GA_MEASUREMENT_ID') or app.config.get('GA_MEASUREMENT_ID')

@app.context_processor
def injectAnalytics():
    return dict(ga_id=_gaId)

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
        xc = request.form.get("xc", type=float)
        yc = request.form.get("yc", type=float)
        domain = request.form.get("xDomain", type=float)
        xcorner = request.form.get("xtopLeft", type=float)
        ycorner = request.form.get("ytopLeft", type=float)
        xcenter = request.form.get("xcenter", type=float)
        ycenter = request.form.get("ycenter", type=float)
        # Start over with the default plot if the session has expired
        # (e.g. browser restarted) or the form values are missing or invalid
        if 'page' not in session or None in (xc, yc, domain, xcorner, ycorner, xcenter, ycenter):
            return redirect(url_for('plotView'))

        # Initialize our plot object and zoom in on the plot area requested
        plot = Mandelbrot(xc, yc, domain)
        plot.zoom(xcorner, ycorner, xcenter, ycenter)

        # Create our image and store the params used to make it
        thePlot = plot.makeImage()
        xc = float(plot.xc)
        yc = float(plot.yc)
        domain = float(plot.domain)
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
    if num >= 0 and num < len(session.get('xc', [])):
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
