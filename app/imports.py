from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import confirm_login, login_user, logout_user, UserMixin, current_user
from . import db, basedir
import datetime
import re
from .utils_and_functions.decorators import login_required, email_required
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import cv2
import numpy
import copy
from PIL import Image