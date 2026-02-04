const http = require("http"); // Built-in module to create an HTTP server
const url = require("url"); // Built-in module to parse URLs

const hostname = "127.0.0.1"; // Localhost IP
const port = 3000; // Port number where the server will listen

// Create an HTTP server
const server = http.createServer((req, res) => {
  // Parse the incoming request URL
  const parsedUrl = url.parse(req.url, true); // 'true' parses query parameters into an object

  // Route: /echo
  // Sends back all request headers as JSON
  if (parsedUrl.pathname === "/echo") {
    res.writeHead(200, { "Content-Type": "application/json" }); // Set response headers
    res.end(JSON.stringify(req.headers)); // Convert headers object to JSON string
  }

  // Route: /slow
  // Delays response for a specified time (ms) from query parameters, default 3s
  else if (parsedUrl.pathname === "/slow") {
    const delay = parseInt(parsedUrl.query.ms) || 3000; // Read 'ms' query param
    setTimeout(() => {
      // Delay sending response
      res.writeHead(200, { "Content-Type": "text/plain" });
      res.end(`Delayed for ${delay}ms`); // Send plain text after delay
    }, delay);
  }

  // Route: /cache
  // Demonstrates cache-control headers
  else if (parsedUrl.pathname === "/cache") {
    res.writeHead(200, {
      "Content-Type": "text/plain", // Response is plain text
      "Cache-Control": "public, max-age=3600", // Browser can cache for 1 hour
      Expires: new Date(Date.now() + 3600 * 1000).toUTCString(), // Expiry time
      "Last-Modified": new Date().toUTCString(), // Last modified timestamp
    });
    res.end("Cache headers set"); // Response body
  }

  // Route: anything else
  else {
    res.writeHead(404, { "Content-Type": "text/plain" }); // Not Found
    res.end("Not Found");
  }
});

// Start the server and listen on the specified hostname and port
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
