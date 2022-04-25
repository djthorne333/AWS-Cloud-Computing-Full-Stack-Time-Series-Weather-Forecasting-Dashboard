from flask import Flask, render_template
app = Flask(__name__, template_folder='Templates', static_folder='cloudpic')



@app.route('/')
def index():
    return render_template('pageS3.html')


#can leave this commented out becuase gunicorn is in charge
#if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=443)



