from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about')
def printabout():
    author='Diksha Wali'
    return render_template('about.html', au=author)

@app.route('/bootstrap')
def printbs():
    # author='Diksha Wali'
    return render_template('bootstrap .html')

app.run(debug=True)

 