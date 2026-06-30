import fastapi

router = fastapi.APIRouter()
users = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    },
    {
        "id": 2,
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
]

@router.get("/users")
async def get_users():
    return users

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user