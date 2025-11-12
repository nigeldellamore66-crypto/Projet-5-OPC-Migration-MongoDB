# MongoDB root user
MONGO_ADMIN="admin"
ADMIN_PWD="admin123"

# Infos DB
DB_NAME="healthcare"
COLLECTION_NAME="patients"

# MongoDB user
MONGO_USER="healthcare_app"
MONGO_PWD="password123"


# Construction des URI de connexion
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PWD}@mongo:27017/{DB_NAME}?authSource=admin"
MONGO_ADMIN_URI = f"mongodb://{MONGO_ADMIN}:{ADMIN_PWD}@mongo:27017/admin"