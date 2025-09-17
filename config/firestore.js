const { Firestore } = require('@google-cloud/firestore');

// Production configuration for Google Cloud Run
const db = new Firestore({
  projectId: process.env.GOOGLE_CLOUD_PROJECT || 'orchestratex-app',
  ignoreUndefinedProperties: true
});

console.log('🔥 Firestore initialized for project:', process.env.GOOGLE_CLOUD_PROJECT || 'orchestratex-app');
module.exports = db;
