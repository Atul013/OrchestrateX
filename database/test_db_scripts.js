#!/usr/bin/env node

// Test script to validate MongoDB setup scripts
// Run with: node test_db_scripts.js

const { MongoClient } = require('mongodb');

const connectionString = 'mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin';

async function testConnection() {
    console.log('🔍 Testing MongoDB connection and setup scripts...\n');
    
    let client;
    try {
        // Connect to MongoDB
        client = new MongoClient(connectionString);
        await client.connect();
        console.log('✅ Connected to MongoDB successfully');
        
        const db = client.db('orchestratex');
        
        // Test collections exist
        const collections = await db.listCollections().toArray();
        console.log(`📁 Found ${collections.length} collections:`);
        collections.forEach(col => console.log(`   - ${col.name}`));
        
        // Test AI models
        const aiModels = await db.collection('ai_model_profiles').find({}).toArray();
        console.log(`🤖 Found ${aiModels.length} AI models:`);
        aiModels.forEach(model => 
            console.log(`   - ${model.model_name} (${model.provider}) - ${model.specialties.join(', ')}`)
        );
        
        // Test indexes
        const indexes = await db.collection('ai_model_profiles').indexes();
        console.log(`📊 Found ${indexes.length} indexes on ai_model_profiles collection`);
        
        // Validate required fields
        const missingFields = [];
        for (const model of aiModels) {
            if (!model.model_version) missingFields.push(`${model.model_name}: missing model_version`);
            if (!model.api_endpoint) missingFields.push(`${model.model_name}: missing api_endpoint`);
            if (!model.performance_metrics) missingFields.push(`${model.model_name}: missing performance_metrics`);
        }
        
        if (missingFields.length === 0) {
            console.log('✅ All AI models have required fields');
        } else {
            console.log('❌ Missing fields found:');
            missingFields.forEach(field => console.log(`   - ${field}`));
        }
        
        console.log('\n🎉 Database setup validation completed successfully!');
        
    } catch (error) {
        console.error('❌ Error testing database setup:', error.message);
        process.exit(1);
    } finally {
        if (client) {
            await client.close();
            console.log('🔐 Database connection closed');
        }
    }
}

// Run the test if this script is executed directly
if (require.main === module) {
    testConnection();
}

module.exports = { testConnection };
