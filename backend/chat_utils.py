from backend import models


def save_message(db, user_id: int, role: str, content: str):
    msg = models.Message(
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()

def get_chat_history(db, user_id: int, limit: int = 10):
    return (
        db.query(models.Message)
        .filter(models.Message.user_id == user_id)
        .order_by(models.Message.created_at.asc())
        .limit(limit)
        .all()
    )
