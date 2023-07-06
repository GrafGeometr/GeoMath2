from app.imports import *
from app.model_imports import *
from app.utils_and_functions.token_gen import generate_token
from app.utils_and_functions.send_letter import send_email




def email_validity_checker(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return (bool(re.fullmatch(regex, email)))

def get_current_user():
    return User.query.filter_by(name = current_user.name).first()

def email_token_stuff(email_obj):
    print(email_obj)

    token = generate_token(30)
    email_obj.token = token
    try:
        send_email(email_obj.name, url_for("emv.verify", username=email_obj.user.name, email_name=email_obj.name, email_token=token, _external=True))
    except Exception as e:
        print(e)




# If everything is OK, saves file to dir and returns filename
# Otherwise, I mean:
# - If file is a VIRUS
# - If file is broken
# - If file is too big (> maxsize in bytes)
# returns None
def safe_image_upload(files, directory, maxsize=2*1024*1024):
    result = []
    for file in files:
        try:
            # grab image
            profile_pic = file
            if profile_pic is None:
                raise Exception
            # grab image name (removing suspicious chars)
            pic_filename = secure_filename('.'.join(profile_pic.filename.split('.')[:-1]))+"."+profile_pic.filename.split('.')[-1]
            # set UUID (unique name)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            path = os.path.join(directory, pic_name)
            # check if it is not a VIRUS!!!
            tmp_image = None
            try:
                tmp_image = cv2.imdecode(numpy.fromstring(profile_pic.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                checker = tmp_image.shape
            except:
                raise Exception
            # at least it isn't a VIRUS, we can save it
            cv2.imwrite(path, tmp_image)
            
            # but it may be too big
            if os.stat(path).st_size > maxsize:
                os.remove(path)
                raise Exception
            # well, you've won this time
            result.append(pic_name)
        except:
            result.append(None)
    return result