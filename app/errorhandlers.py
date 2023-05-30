# -*- coding: utf-8 -*-
from .imports import *
from .model_imports import *

err = Blueprint('err', __name__)

@err.errorhandler(401)
def unauthorized_error(error):
    return render_template('base.html')