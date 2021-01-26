# Generate Mandelbrot set. Return it as a string that can be 
# passed to an html img tag
#     Copyright (C) 2021 Rick Eichhorn: rickapps@live.com

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
from PIL import Image
import colorsys
from io import BytesIO
from base64 import b64encode

class Mandelbrot:
    'Create an image to plot for Mandelbrot set'
    _imageLength = 720  # Image length in pixels. Change css if you change dims
    _imageHeight = 540  # Image height in pixels.
    _iterations = 100   # Length of series to generate to test for convergence
    _testDistance = 4   # Used to test for convergence
    _saturation = 0.7   # Used for color 0 to 1. Zero full grey, One no grey
    _brightness = 1.0   # Color brightness 0 to 1.

    def __init__(self, xc, yc, domain):
        self.xc = xc
        self.yc = yc
        self.domain = domain
        # Calculate xMin, yMax, xScale, yScale
        self.setScale()
        return

    def zoom(self, xcorner, ycorner, xcenter, ycenter):
        'Zoom in on existing image and replot.'
        # Input coords are in terms of pixels. ycenter is
        # negative at top of screen, zero at bottom.
        self.xc = self.xMin + (xcenter * self.xScale)
        self.yc = self.yMin + (ycenter * self.yScale)
        # Get our new domain
        self.domain = 2 * (xcenter - xcorner) * self.xScale
        # Calculate new scale factors based on our new domain
        self.setScale()
        return


    def setScale(self):
        # Use aspect ratio to figure out yRange
        yRange = self.domain * Mandelbrot._imageHeight / Mandelbrot._imageLength 
        self.xMin = self.xc - self.domain/2.0
        self.yMin = self.yc - yRange/2.0
        self.xScale = self.domain/Mandelbrot._imageLength
        self.yScale = -self.xScale #(Equivalent to: yRange/Mandelbrot._imageHeight)
        return

    def makeImage(self):
        # Initialize our image to black
        img = Image.new('RGB',(Mandelbrot._imageLength,Mandelbrot._imageHeight), color='black')
        pixels = img.load()

        # Loop through every pixel in the image
        for row in range(Mandelbrot._imageHeight):
            for col in range(Mandelbrot._imageLength):
                # Convert to (x,y) coords. (row, col) starts at top left
                # We want min (x,y) to be at bottom left
                srow = row - (Mandelbrot._imageHeight - 1)
                xComplex = self.xMin + col * self.xScale
                yComplex = self.yMin + srow * self.yScale
                # We are going to generate our series using this value as our constant.
                # It is a complex number (a+bi) defined as (xComplex, yComplex)
                # We will generate up to iterations terms of the series for
                # each complex number. Note that (a+bi)**2 = a**2 + 2abi - b**2
                x = xComplex # We need a starting value
                y = yComplex # We need a starting value to generate next val in series
                for i in range(Mandelbrot._iterations + 1):
                    a = x*x - y*y # First generate (a+bi)**2 using previous (x,y)
                    b = 2 * x * y
                    x = a + xComplex  # New series values are old value squared plus
                    y = b + yComplex  # our constant complex number.
                    # Check if series is diverging
                    if (x * x) + (y * y) > Mandelbrot._testDistance:
                        break

                # If we exited the loop early, our series diverged
                if i < Mandelbrot._iterations:
                    # Get fraction of loop we completed. Higher values
                    # mean slower divergence
                    fraction = (i+1)/Mandelbrot._iterations
                    # We use HSV color model here. Then we convert it to rgb.
                    hue = fraction   # Between 0 and 1. Progresses Red, Yellow, Green, Cyan, Blue, Magenta
                    rgb = tuple(round(i*255) for i in colorsys.hsv_to_rgb(
                        hue, Mandelbrot._saturation, Mandelbrot._brightness))
                    # Set the pixel to the color we calculated. We use row here instead
                    # of srow so our image is not up-side-down.
                    pixels[col,row] = rgb 
        pngImage = BytesIO()
        img.save(pngImage, 'PNG')
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String                     

if __name__== "__main__":
    plot = Mandelbrot(-0.65, 0.0, 3.4)
    plot.makeImage()
