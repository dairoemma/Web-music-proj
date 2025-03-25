from celery import Celery
from config import Config
from datetime import datetime
import time

celery = Celery(
        __name__,
        backend= Config.CELERY_BACKEND_URL ,
        broker= Config.CELERY_BROKER_URL
    )

def make_celery(app):
    celery.conf.update(app.config)
    return celery



@celery.task()
def process_payment(account_name, account_number, cvv, password, user_expiry_date, amount_in_account):
    
    try: 

        expiry_date_min = datetime.strptime("01/10/2025", "%d/%m/%Y")
        if  not account_name:
            raise ValueError("Account name required")
        if  not account_number:
            raise ValueError("Account_number required")
        if not cvv:
            raise ValueError("Cvv required")
        if not password:
            raise ValueError("Password required")
        if amount_in_account < 100:
            raise ValueError("Insufficient balance")
        if user_expiry_date < expiry_date_min:
             raise ValueError("Card has expired")
        
        time.sleep(3)
        return {"status": "success", "message": "Payment processing started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}




    
