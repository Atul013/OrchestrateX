// OrchestrateX User Management Script
// Creates application users with appropriate permissions

print("🔐 Starting OrchestrateX User Management Setup...");

// Switch to admin database for user creation
db = db.getSiblingDB("admin");

// Create application user for OrchestrateX backend
try {
    db.createUser({
        user: "orchestratex_app",
        pwd: "orchestratex_app_password_2024",
        roles: [
            {
                role: "readWrite",
                db: "orchestratex"
            },
            {
                role: "dbAdmin",
                db: "orchestratex"
            }
        ],
        mechanisms: ["SCRAM-SHA-1", "SCRAM-SHA-256"]
    });
    print("✅ Created application user: orchestratex_app");
} catch (error) {
    if (error.code === 51003) { // User already exists
        print("ℹ️  Application user already exists: orchestratex_app");
    } else {
        print("❌ Error creating application user: " + error.message);
    }
}

// Create read-only user for analytics and reporting
try {
    db.createUser({
        user: "orchestratex_readonly",
        pwd: "orchestratex_readonly_password_2024",
        roles: [
            {
                role: "read",
                db: "orchestratex"
            }
        ],
        mechanisms: ["SCRAM-SHA-1", "SCRAM-SHA-256"]
    });
    print("✅ Created read-only user: orchestratex_readonly");
} catch (error) {
    if (error.code === 51003) { // User already exists
        print("ℹ️  Read-only user already exists: orchestratex_readonly");
    } else {
        print("❌ Error creating read-only user: " + error.message);
    }
}

// Create backup user for database maintenance
try {
    db.createUser({
        user: "orchestratex_backup",
        pwd: "orchestratex_backup_password_2024",
        roles: [
            {
                role: "backup",
                db: "admin"
            },
            {
                role: "restore",
                db: "admin"
            },
            {
                role: "read",
                db: "orchestratex"
            }
        ],
        mechanisms: ["SCRAM-SHA-1", "SCRAM-SHA-256"]
    });
    print("✅ Created backup user: orchestratex_backup");
} catch (error) {
    if (error.code === 51003) { // User already exists
        print("ℹ️  Backup user already exists: orchestratex_backup");
    } else {
        print("❌ Error creating backup user: " + error.message);
    }
}

// Switch to orchestratex database to set up application-specific configurations
db = db.getSiblingDB("orchestratex");

// Create application-specific roles and permissions
try {
    db.runCommand({
        createRole: "orchestratex_api_role",
        privileges: [
            {
                resource: { db: "orchestratex", collection: "" },
                actions: ["find", "insert", "update", "remove"]
            },
            {
                resource: { db: "orchestratex", collection: "system.indexes" },
                actions: ["find"]
            }
        ],
        roles: []
    });
    print("✅ Created custom role: orchestratex_api_role");
} catch (error) {
    if (error.code === 51002) { // Role already exists
        print("ℹ️  Custom role already exists: orchestratex_api_role");
    } else {
        print("❌ Error creating custom role: " + error.message);
    }
}

// Grant the custom role to the application user
try {
    db.grantRolesToUser("orchestratex_app", ["orchestratex_api_role"]);
    print("✅ Granted custom role to application user");
} catch (error) {
    print("ℹ️  Role assignment: " + error.message);
}

// List all users for verification
print("\n📋 Current Database Users:");
try {
    db = db.getSiblingDB("admin");
    var users = db.getUsers();
    users.forEach(function(user) {
        if (user.user.includes("orchestratex") || user.user === "project_admin") {
            print("👤 User: " + user.user);
            print("   Roles: " + JSON.stringify(user.roles));
        }
    });
} catch (error) {
    print("❌ Error listing users: " + error.message);
}

print("\n🎉 OrchestrateX User Management setup completed!");
print("\n📚 Available Users:");
print("🔑 Root Admin: project_admin (full access)");
print("🛠️  Application: orchestratex_app (read/write access)");
print("👁️  Read-only: orchestratex_readonly (analytics access)");
print("💾 Backup: orchestratex_backup (backup/restore access)");

print("\n🔗 Connection Examples:");
print("Application: mongodb://orchestratex_app:orchestratex_app_password_2024@localhost:27018/orchestratex");
print("Read-only: mongodb://orchestratex_readonly:orchestratex_readonly_password_2024@localhost:27018/orchestratex");
print("Admin: mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin");
