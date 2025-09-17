const http = require('http');

console.log('Testing server connectivity...');

const req = http.get('http://localhost:8002/health', (res) => {
  console.log(`Status Code: ${res.statusCode}`);
  console.log(`Headers:`, res.headers);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('Response:', data);
    process.exit(0);
  });
});

req.on('error', (err) => {
  console.log('Error:', err.message);
  process.exit(1);
});

req.setTimeout(5000, () => {
  console.log('Request timeout');
  req.destroy();
  process.exit(1);
});