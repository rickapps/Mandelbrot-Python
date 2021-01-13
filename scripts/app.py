from flask import Flask, render_template
from mandelbrot import drawBrot

app = Flask(__name__)

@app.route("/", methods=["GET"])
def plotView():
  
    pngImageB64String = drawBrot(-0.65, 0.0, 3.4)      
    return render_template("index.html", image=pngImageB64String)

if __name__ == "__main__":
    app.run()
