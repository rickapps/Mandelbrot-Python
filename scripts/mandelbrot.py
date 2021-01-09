# Generate Mandelbrot set
from PIL import Image
import colorsys
import math
import os

def drawBrot(xc, yc, domain):
    # Define some constants
    # Number of pixels in our image
    imageLength = 1600
    imageHeight = 1200
    # Used to determine if series diverges
    iterations = 700
    testDistance = 4

    # Calculate the rest of our constants
    aspectRatio = imageLength / imageHeight
    yRange = domain / aspectRatio
    xMin = xc - domain/2
    yMax = yc + yRange/2 
    xScale = domain/imageLength
    yScale = yRange/imageHeight

    # Initialize our image to black
    img = Image.new('RGB',(imageLength,imageHeight), color='black')
    pixels = img.load()

    # Loop through every pixel in the image
    for row in range(imageHeight):
        for col in range(imageLength):
            # Convert to (x,y) coords. (row, col) starts at top left
            # We want min (x,y) to be at bottom left
            xComplex = xMin + col * xScale
            yComplex = yMax - row * yScale
            # We are going to generate our series using this value as our constant.
            # It is a complex number (a+bi) defined as (xComplex, yComplex)
            # We will generate up to iterations terms of the series for
            # each complex number. Note that (a+bi)**2 = a**2 + 2abi - b**2
            x = xComplex # We need a starting value
            y = yComplex # We need a starting value to generate next val in series
            for i in range(iterations + 1):
                a = x*x - y*y # First generate (a+bi)**2 using previous (x,y)
                b = 2 * x * y
                x = a + xComplex  # New series values are old value squared plus
                y = b + yComplex  # our constant complex number.
                # Check if series is diverging
                if (x * x) + (y * y) > testDistance:
                    break

            # If we exited the loop early, our series diverged
            if i < iterations:
                # Get fraction of loop we completed. Higher values
                # mean slower divergence
                fraction = (i+1)/iterations
                hue = fraction   # Between 0 and 1. Progresses Red, Yellow, Green, Cyan, Blue, Magenta
                saturation = 0.7   # Amount of grey - zero is all grey, one is no grey
                value = 1        # Brightness, zero is black, 1 is full brightness
                rgb = tuple(round(i*255) for i in colorsys.hsv_to_rgb(hue,saturation,value))
                # Set the pixel to the color we calculated
                pixels[col,row] = rgb                      
    # Shows image in a separate window
    img.show()  
    # Shows image inline
    #imshow(np.asarray(img))  
    #img.save('output.png')
    #os.system('open output.png')  

if __name__== "__main__":
  drawBrot(-0.65, 0.0, 3.4)      