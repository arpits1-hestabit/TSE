const http = require('http');
const url = require('url');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);

    if (parsedUrl.pathname === '/echo') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(req.headers));
    } 
    else if (parsedUrl.pathname === '/slow') {
        const delay = parseInt(parsedUrl.query.ms) || 3000;
        setTimeout(() => {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end(`Delayed for ${delay}ms`);
        }, delay);
    } 
    else if (parsedUrl.pathname === '/cache') {
        res.writeHead(200, {
            'Content-Type': 'text/plain',
            'Cache-Control': 'public, max-age=3600',
            'Expires': new Date(Date.now() + 3600 * 1000).toUTCString(),
            'Last-Modified': new Date().toUTCString(),
        });
        res.end('Cache headers set');
    } 
    else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
