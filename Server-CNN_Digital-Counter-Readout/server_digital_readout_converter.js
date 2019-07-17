var http = require('http');
var url = require('url');
var fs = require('fs');
var opencv = require('opencv4nodejs');

var readCounter = require("./lib/lib_read_digital_counter");

var ImageResize = function(input, output)
{
    // Resize Image to 32x20 pixel - required input for the neural network
    var im = opencv.imread(input).resize(32,20);
    opencv.imwrite(output, im);
}

var abfrage = function(req, res) {
    var q = url.parse(req.url, true).query;
    var filename = q.url;

    if (filename)
    {
        console.log(filename);
        var file_download = fs.createWriteStream("./image/original.jpg");
        http.get(filename, (response) => {response.pipe(file_download);});

        file_download.on('finish', function(){
            file_download.end();

            ImageResize("./image/original.jpg", "./image/resize.jpg");
     
            readCounter.Readout('./image/resize.jpg').then(result => {
                console.log('Counter Readout: ' + result);

                res.writeHead(200, {'Content-Type': 'text/html'});
                var txt = "";
                txt += 'Original: <p><img src=/image/original.jpg></img><p>';
                txt += 'Resize (20x32): <p><img src=/image/resize.jpg></img><p>';
                txt += "Counter_Readout:\t" + result;

                res.end(txt);}
                )
        });
    }

    if ((req.url == '/image/resize.jpg') || (req.url == '/image/original.jpg'))
    {
        var s = fs.createReadStream("." + req.url);
        s.on('open', function () {
            res.setHeader('Content-Type', 'image/jpeg');
            s.pipe(res);
        });
    }
}

http.createServer(abfrage).listen(3000);
