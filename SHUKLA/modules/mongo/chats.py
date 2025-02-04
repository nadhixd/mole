from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Connection URI (Replace with your actual database URI)
MONGO_URI = "mongodb+srv://khushijha5544:karan2020@krishnauff.ndruqrp.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["SHUKLA_DB"]  # Database Name
chat_collection = db["chats"]  # Collection Name

async def get_chat_id(user_id: int) -> int:
    """
    Retrieve the chat ID associated with a user ID.
    Returns 0 if no chat ID is found.
    """
    chat_data = await chat_collection.find_one({"user_id": user_id})
    return chat_data["chat_id"] if chat_data else 0

async def set_chat_id(user_id: int, chat_id: int):
    """
    Store or update a chat ID for a user.
    """
    await chat_collection.update_one(
        {"user_id": user_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True
    )