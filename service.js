/**
 * Backend Service Entry Point
 * Project: Azure Load Testing Capacity Study (24CC3046-P056)
 * Supports Node.js 24 LTS and Azure App Service
 */

require('dotenv').config();
const app = require('./src/server');
const { startServer } = require('./src/server');

module.exports = app;
module.exports.startServer = startServer;

if (require.main === module) {
  const PORT = process.env.PORT || 8080;
  startServer(PORT).catch(err => {
    console.error('Fatal error starting server:', err);
    process.exit(1);
  });
}
