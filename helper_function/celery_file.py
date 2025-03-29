# from celery import Celery  #no longer used celery because couldn't add a background worker during deployment
# from config import Config
from datetime import datetime  #importing necessary dependencies
import time

# celery = Celery(
#         __name__,
#         backend= Config.CELERY_BACKEND_URL ,
#         broker= Config.CELERY_BROKER_URL
#     )

# def make_celery(app):
#     celery.conf.update(app.config)
#     return celery



# @celery.task()   #this function was to handle the payment as async with celery but unfortunately we couldn't, but it still process the payment
def process_payment(account_name, account_number, cvv, password, user_expiry_date, amount_in_account):
    
    try: 

        expiry_date_min = datetime.strptime("01/10/2025", "%d/%m/%Y") # initialized minimum expiry date 
        # checking if all inputs are valid
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
        
        time.sleep(3) #this was set to add a time interval between the payment process started and the payment processed. after details entered are valid, it takes three seconds and then sends the response
        return {"status": "success", "message": "Payment processing started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}




    
