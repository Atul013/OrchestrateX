// Initialization script for OrchestrateX MongoDB
// Creates application database user with least privileges

const dbName = 'orchestratex';
const appUser = 'appuser';
const appPass = 'appPasswordDev!';

const db = db.getSiblingDB(dbName);

// Create application user with readWrite on the db
try {
  db.createUser({
    user: appUser,
    pwd: appPass,
    roles: [ { role: 'readWrite', db: dbName } ]
  });
  print(`Created user ${appUser} for database ${dbName}`);
} catch (e) {
  print('User creation skipped or failed:', e.message);
}

// Example collection and index setup
const collections = [
  { name: 'prompts', indexes: [ { key: { domain: 1 }, name: 'idx_domain' }, { key: { hash: 1 }, name: 'idx_hash', unique: true } ] },
  { name: 'responses', indexes: [ { key: { prompt_id: 1, model: 1 }, name: 'idx_prompt_model', unique: true } ] },
  { name: 'ratings', indexes: [ { key: { response_id: 1 }, name: 'idx_response' }, { key: { annotator_id: 1 }, name: 'idx_annotator' } ] }
];

collections.forEach(cfg => {
  const c = db.getCollection(cfg.name);
  if (!c) {
    db.createCollection(cfg.name);
  }
  cfg.indexes.forEach(ix => {
    try {
      c.createIndex(ix.key, { name: ix.name, unique: ix.unique || false });
    } catch (err) {
      print('Index creation error for', ix.name, err.message);
    }
  });
});

print('Initialization script completed.');
