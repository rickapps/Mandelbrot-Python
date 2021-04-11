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
import numpy as np
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

    def setColor(self, iterations):
        # Get fraction of loop we completed. Higher values
        # mean slower divergence
        if iterations >= Mandelbrot._iterations:
            return (0,0,0)
        fraction = (iterations)/Mandelbrot._iterations
        # We use HSV color model here. Then we convert it to rgb.
        hue = fraction   # Between 0 and 1. Progresses Red, Yellow, Green, Cyan, Blue, Magenta
        rgb = tuple(round(i*255) for i in colorsys.hsv_to_rgb(
            hue, Mandelbrot._saturation, Mandelbrot._brightness))
        return rgb

    def setScale(self):
        # Use aspect ratio to figure out yRange
        yRange = self.domain * Mandelbrot._imageHeight / Mandelbrot._imageLength 
        self.xMin = self.xc - self.domain/2.0
        self.xMax = self.xMin + self.domain
        self.yMin = self.yc - yRange/2.0
        self.yMax = self.yMin + yRange
        self.xScale = self.domain/Mandelbrot._imageLength
        self.yScale = -self.xScale #(Equivalent to: yRange/Mandelbrot._imageHeight)
        return

    def makeImage(self):
        # Initialize our image to black
        img = Image.new('RGB',(Mandelbrot._imageLength,Mandelbrot._imageHeight), color='black')
        Colors = []
        for i in range(Mandelbrot._iterations + 1):
            Colors.append(self.setColor(i))

        # Get all our x values
        xComplex = np.linspace(self.xMin, self.xMax, num=Mandelbrot._imageHeight) \
            .reshape((1,Mandelbrot._imageHeight)) 
        # Get our y values (imaginary) as a vector
        yComplex = np.linspace(self.yMin, self.yMax, num=Mandelbrot._imageLength) \
            .reshape((Mandelbrot._imageLength, 1))
        # Stick the two together into a matrix
        C = np.tile(xComplex, (Mandelbrot._imageLength, 1)) \
            + 1j * np.tile(yComplex, (1, Mandelbrot._imageHeight))
        # Now we have all the complex numbers for our image in an array
        # where each position cooresponds to a pixel in our image
        # We will iterate on each member to see if it converges or not
        Z = np.zeros((Mandelbrot._imageLength, Mandelbrot._imageHeight), dtype=complex)
        M = np.full((Mandelbrot._imageLength, Mandelbrot._imageHeight), True, dtype=bool)
        # Make a record of our iterations. We will use this to make our image
        I = np.zeros((Mandelbrot._imageLength,Mandelbrot._imageHeight,3), dtype=np.uint8)
        for i in range(Mandelbrot._iterations + 1):
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z) > 2] = False
            I[M] = Colors[i]

        img = Image.fromarray(np.flipud(I))
        pngImage = BytesIO()
        img.save(pngImage, 'PNG')
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String                     

if __name__== "__main__":
    plot = Mandelbrot(-0.65, 0.0, 3.4)
    plot.makeImage()
