# Pyhton server using an neural network with tensorflow
Details on setup and training of the CNN neural network

## Version
##### 1.0 Initial Version
##### 2.0 Transfer from Node.JS to Python
* Transfer from NodeJS to Python
* Implementation of configuration file and log-Algorithm

To run the Python code copy the whole [code](code) directory including subdirectory.

Path are relative, so it should run immediatly with the following command:
* `pip install requirements.txt`
* `python server_readout_digital_digits.py`

### Configuration

The configuration is storred in the subdirectory `config`. In the Ini-file the CNN-Network to be loaded is listed. Configuration of the neural network (*.h5) itself is stored in the subdirectory `neuralnets`.


### Server Usage

The server is listening to port 3000 and accepts requests in the following syntac:

http://server-ip:3000/?url=http://picture-server/image.jpg

* server-ip: address of the server running the script
* parameter "url": url to the picture to be analysed 

The output is the following:

   <img src="./image/server_output.png" width="400">
   


