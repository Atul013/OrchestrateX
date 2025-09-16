const { Firestore } = require('@google-cloud/firestore');

const db = new Firestore({
  projectId: process.env.GOOGLE_CLOUD_PROJECT || 'orchestratex-app'
});

console.log('🔥 Firestore initialized for project:', process.env.GOOGLE_CLOUD_PROJECT || 'orchestratex-app');
module.exports = db;
