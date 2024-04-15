from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class Token(BaseModel):
	token: str
	expiration: datetime


class OAuthRequestForm:
	"""
	https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/


	"""

	def __init__(self, username: str = Form(), password: str = Form()):
		self.username = username
		self.password = password


class RegisterIn(BaseModel):
	first_name: str
	last_name: str
	email: EmailStr
	phone_number: str
	password: str
	phone_country_code: str = Field("1")


class RegisterOut(BaseModel):
	first_name: str
	last_name: str
	email: EmailStr
	phone_number: str
	phone_country_code: str = Field("1")
