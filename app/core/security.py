import asyncio

import bcrypt


async def hash_password(password: str) -> str:
    hashed = await asyncio.to_thread(bcrypt.hashpw, password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return await asyncio.to_thread(
            bcrypt.checkpw, plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except ValueError:
        return False
