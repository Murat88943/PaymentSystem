from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api.controlers.controllers import (
    handle_register, handle_login, handle_profile,
    handle_create_subscription, handle_cancel_subscription,
    handle_refund_subscription, handle_get_subscription,
    handle_check_subscription, handle_create_payment_link,
    handle_refund_payment
)
from backend.api.repositories.database import init_database, create_subscription

app = FastAPI(title="Payment System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_database()


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SubscriptionCreateRequest(BaseModel):
    user_id: str
    plan_type: str
    price: float
    duration_days: int


class SubscriptionCancelRequest(BaseModel):
    subscription_id: str


class SubscriptionRefundRequest(BaseModel):
    subscription_id: str


class PaymentLinkRequest(BaseModel):
    user_id: str
    plan_name: str
    amount: float
    currency: str = "RUB"
    return_url: str = "http://localhost:5173/"
    description: str


class RefundRequest(BaseModel):
    payment_id: str
    amount: float
    currency: str = "RUB"


@app.post('/auth/register/', tags=["Auth"])
async def register(request: RegisterRequest):
    try:
        data = request.dict()
        result = handle_register(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/auth/login/', tags=["Auth"])
async def login(request: LoginRequest):
    try:
        data = request.dict()
        result = handle_login(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.get('/user/profile/', tags=["User"])
async def profile(user_id: str = Query(...)):
    try:
        result = handle_profile(user_id)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=404, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/subscription/create/', tags=["Subscription"])
async def create_subscription_endpoint(request: SubscriptionCreateRequest):
    try:
        data = request.dict()
        result = handle_create_subscription(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/subscription/cancel/', tags=["Subscription"])
async def cancel_subscription(request: SubscriptionCancelRequest):
    try:
        data = request.dict()
        result = handle_cancel_subscription(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/subscription/refund/', tags=["Subscription"])
async def refund_subscription(request: SubscriptionRefundRequest):
    try:
        data = request.dict()
        result = handle_refund_subscription(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.get('/subscription/status/', tags=["Subscription"])
async def subscription_status(user_id: str = Query(...)):
    try:
        result = handle_get_subscription(user_id)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=404, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.get('/subscription/check/', tags=["Subscription"])
async def check_subscription(user_id: str = Query(...)):
    try:
        result = handle_check_subscription(user_id)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/payment/create-link/', tags=["Payment"])
async def create_payment_link(request: PaymentLinkRequest):
    try:
        data = request.dict()
        result = handle_create_payment_link(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/payment/refund/', tags=["Payment"])
async def refund_payment_endpoint(request: RefundRequest):
    try:
        data = request.dict()
        result = handle_refund_payment(data)
        if result.get('success'):
            return JSONResponse(status_code=200, content=result)
        return JSONResponse(status_code=400, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.post('/payment/webhook/', tags=["Payment"])
async def payment_webhook(request: Request):
    try:
        data = await request.json()

        if data.get('event') == 'payment.succeeded':
            payment_data = data.get('object', {})
            metadata = payment_data.get('metadata', {})
            user_id = metadata.get('user_id')
            plan_name = metadata.get('plan_name')
            amount_data = payment_data.get('amount', {})
            price = float(amount_data.get('value', 0))

            if user_id and plan_name:
                create_subscription(user_id, plan_name, price, 30)
                return JSONResponse(status_code=200, content={'success': True})

        return JSONResponse(status_code=200, content={'success': True})
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})


@app.get('/health/', tags=["Health"])
async def health():
    return {'status': 'ok'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)