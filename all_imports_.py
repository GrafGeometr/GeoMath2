from flask import Flask, render_template, redirect, request, make_response
import os
from data.user import User
from data.email import Email
from init_app import app, load_user, website_link
from utils_and_functions.decorators import route, email_required
from utils_and_functions.usefull_functions import *
from data import db_session
from utils_and_functions.token_gen import generate_token
from utils_and_functions.send_letter import send_email



from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
