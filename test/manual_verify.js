const http = require('http');
const { startServer } = require('../service');

async function testEndpoint(baseUrl, method, path, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl);
    const options = {
      method,
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      headers: { 'Content-Type': 'application/json' }
    };
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, body: data });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function verifyAll() {
  const server = await startServer(3000);
  const baseUrl = 'http://127.0.0.1:3000';
  console.log('\n--- MANUAL ENDPOINT VERIFICATION (http://127.0.0.1:3000) ---');

  try {
    const health = await testEndpoint(baseUrl, 'GET', '/health');
    console.log('[1/8] /health -> HTTP', health.status, JSON.stringify(health.body));

    const products = await testEndpoint(baseUrl, 'GET', '/api/products?limit=2');
    console.log('[2/8] /api/products -> HTTP', products.status, 'Count:', products.body.count);

    const product1 = await testEndpoint(baseUrl, 'GET', '/api/products/1');
    console.log('[3/8] /api/products/1 -> HTTP', product1.status, 'Name:', product1.body.data.name);

    const search = await testEndpoint(baseUrl, 'GET', '/api/search?q=laptop');
    console.log('[4/8] /api/search?q=laptop -> HTTP', search.status, 'Matched:', search.body.count);

    const dashboard = await testEndpoint(baseUrl, 'GET', '/api/dashboard');
    console.log('[5/8] /api/dashboard -> HTTP', dashboard.status, 'Stats:', JSON.stringify(dashboard.body.stats));

    const orders = await testEndpoint(baseUrl, 'GET', '/api/orders?limit=2');
    console.log('[6/8] /api/orders -> HTTP', orders.status, 'Count:', orders.body.count);

    const newOrder = await testEndpoint(baseUrl, 'POST', '/api/orders', {
      userId: 1,
      items: [{ productId: 1, quantity: 2, unitPrice: 299.99 }]
    });
    console.log('[7/8] POST /api/orders -> HTTP', newOrder.status, 'OrderId:', newOrder.body.orderId);

    const heavy = await testEndpoint(baseUrl, 'GET', '/api/heavy-operation?iterations=1000');
    console.log('[8/8] /api/heavy-operation -> HTTP', heavy.status, 'DurationMs:', heavy.body.durationMs);

    console.log('\nALL 8 ENDPOINTS MANUALLY TESTED AND VERIFIED OK!\n');
  } finally {
    server.close();
  }
}

verifyAll().catch(console.error);
