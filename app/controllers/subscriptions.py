from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import get_db
from app.middleware.dependencies import require_minecraft_cookie

router = APIRouter()


@router.get("/{world_id}")
async def get_subscription(
    world_id: int,
    cookie: str = Depends(require_minecraft_cookie),
    db: Session = Depends(get_db)
):
    """Get subscription for a world"""
    from app.models.entities import World
    from datetime import datetime, timedelta
    
    world = db.query(World).filter(World.Id == world_id).first()
    if not world or not world.Subscription:
        return {"subscriptionType": "NORMAL", "daysLeft": 30}
    
    days_left = (world.Subscription.StartDate + timedelta(days=30) - datetime.now()).days
    return {
        "subscriptionType": world.Subscription.SubscriptionType,
        "daysLeft": max(0, days_left)
    }
