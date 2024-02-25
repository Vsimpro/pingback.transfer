import os, json, base64

from flask import Flask
from flask_cors import CORS

#
#   Global Variables
#
received_messages = []

#
#   FLASK
#
app = Flask(__name__)
CORS(app)


def append_to( filename, data ):
    contents = b""

    if os.path.exists( filename ):
        with open( filename, "rb+" ) as file:
            contents = file.read()

    with open( filename, "wb+" ) as file:
        file.write( contents )
        
        if data not in contents:
            file.write( data )

    return


def refinery( msg ) -> bool:
    try:
        data = base64.b64decode( msg ).decode("utf-8").replace("'", '"')

        # Check if a dict
        try:
            data = json.loads( data )

        except Exception as e:
            print( f"(refienry) Ran into an exception, e:", e )
            exit( 2 )
            return False

        filedata = data[ "data" ].replace( "%2B", "+" ).replace( "%99", "/" )
        filename = data[ "filename" ]
        full_path = "./output/" + filename

        filedata = base64.b64decode( filedata )
        append_to( full_path, filedata )

    except Exception as e:
        print( f"[refinery] Ran into an exception, e:", e )
        return False

    return True



@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/listener/<file>')
@app.route('/listener/<file>/')
def message( file ):
    global received_messages
    
    file = file.replace( "%99", "/" )
    file = file.replace( "%2B", "+" )
    try:
        print( f"(listener) RECEIVED: " )
        print( f"(listener)\t RAW:",     file )
        print( f"(listener)\t DECODED:", base64.b64decode( file ).decode("utf-8") )
        print( f"(listener)\t Sending to refinery.." )
        print()

        refinery( file )
        
        received_messages.append( file )

    except Exception as e:
        print( f"(listener) Ran into an exception, e:", e )

    print( f"(listener) Flask response: ")
    return 'Hello, World!'


if __name__ == "__main__":
    app.run("0.0.0.0", "5500")
    print( f"(listener) started to listen.. " )