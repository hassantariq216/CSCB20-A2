from flask import Flask, render_template, escape, request

app = Flask(__name__)

@app.route('/', defaults={'name': 'human'})
@app.route('/<name>')
def generateResponse(name):

    if (name.isalpha()):
        return """
            <html><body>
            <h1>Welcome, {0}, to my CSCB20 Website!</h1>
            </body></html>
            """.format(
                (           
                    "".join(filter(str.isalpha, name))).swapcase()
                )

    return """

        <html><body>

        <h1>Welcome, {0}, to my CSCB20 Website!</h1>
        </body></html>
        """.format(
           (       	
              "".join(filter(str.isalpha, name)))
           ) 

if __name__ == "__main__":
    app.run()


