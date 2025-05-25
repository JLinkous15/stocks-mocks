from fastapi import APIRouter, Depends
from dependencies import get_sns_client

router = APIRouter()

@router.post("/alert")
async def send_alert(sns=Depends(get_sns_client)):
    sns.publish(
        TopicArn="your-topic-arn",
        Message="Trend is bullish!"
    )
    return {"status": "sent"}
