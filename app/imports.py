from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import confirm_login, login_user, logout_user, UserMixin, current_user
from . import db
import datetime
import re
from .utils_and_functions.decorators import login_required, email_required