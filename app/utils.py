from fastapi import HTTPException

def verify_bearer_token(authorization: str, expected_token: str = "lanzhengpeng") -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing Bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    if token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    return token
