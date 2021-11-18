import re


def IsMissingFields(data,required_fields):
    '''
    It takes a list required_fields as input
    and returns a tuple (status,reason) if 
    status is true it returns None else returns
    first missing fields with reason as status.
    '''
    for field in required_fields:
        try:
            temp = data[field]
            if temp == '' or temp == None:
                return(False,f"Null Value for field {field}")
        except:
            return(False,f"{field} field not present.")
    return (True,None)



def isValidName(name):
    '''
    For check of first_name and last_name
    both can only be alphabets without spaces
    a total of 38 chars length(19 for each)
    returns true if both conditions True
    '''
    return name.isalpha() and len(name)<20



def isValidPass(pass1,pass2):
    message = '''
    Password should be strong:
    1. minimum 1 capital letter
    2. minimum 1 small letter
    3. minimum 1 digit
    4. minimum 1 special chars
    5. minimum length 8
    6. maximum length 20
    7. both passwords should be match
    '''
    status = [False for i in range(7)]
    if(len(pass1)) >= 8:
        status[4] = True

    if len(pass1) <= 20:
        status[5] = True

    for letter in pass1:
        if ord(letter) in range(65,91):
            status[0] = True
        elif ord(letter) in range(97,123):
            status[1] = True
        elif ord(letter) in range(48,58):
            status[2] = True
        else:
            status[3] = True
    
    if pass1 == pass2:
        status[6] = True
    
    if len(list(set(status))) == 1 and list(set(status))[0]:
        return (True,None)
    else:
        return (False,message)


def isValidMail(email):
    '''
    uses Regex to check if provided mail id
    is in a General Mail Id format or not
    returns True if it is else False
    '''
    mail_type = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(mail_type, email)):
        return True
    else:
        return False