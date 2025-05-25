from lambdas import sns_client
from fastapi import Depends

def get_sns_client():
    return sns_client
