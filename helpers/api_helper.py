from django.db.models import TextChoices

class API_Messages():
    EMAIL_EXISTS="Email Already exists. Please Login"
    EMAIL_DOESNOT_EXIST="EMAIL doesn't exist, please Register"
    SUCCESSFUL_REGISTRATION="Successfully Registered"
    INCORRECT_PASSWORD="Password is incorrect. Please check it"
    SUCCESSFUL_LOGIN="Successfully LoggedIn"
    SUCCESSFUL_LOGOUT="Successfully LoggedOut"
    SESSION_EXPIRED="Session Expired"
    PROFILE_UPDATED="Profile Updated Successfully"
    LINK_BROKEN="Link Broken"
    KEYS_GENERATED="Keys Generated Successfully"
    FILE_UPLOADED="File Encrypted & Sent Successfully"
    FILE_DOWNLOADED="File Downloaded & Decrypted Successfully"


def api_response(response_type,api_message,data=None):
    d={}
    d['response_type']=response_type
    d['api_message']=api_message
    if(data):
        d['data']=data
    return d


class ResponseType(TextChoices):
    SUCCESS="Success"
    FAILED="Failed"