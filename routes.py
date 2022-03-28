from fastapi import HTTPException, Security, APIRouter
from deta import Deta


from auth import Auth
from Models.auth_model import AuthModel
from Models.book_model import BookModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()
deta = Deta("a01rek6x_uoMgF7eRCoDyPAPzfAJQNXTsVAyCcb4s")
users_db = deta.Base('users')
books_db = deta.Base('books')


@router.post('/signup')
def signup(user_detais: AuthModel):
    if users_db.get(user_detais.email) != None:
        return 'Account already exists'
    try:
        hashed_password = auth_handler.encode_password(user_detais.password)
        user = {'key': user_detais.email, 'password': hashed_password}
        return users_db.put(user)
    except:
        error_msg = 'Failed to signup user'
        return error_msg


@router.post('/login')
def login(user_details: AuthModel):
    user = users_db.get(user_details.email)
    if user is None:
        return HTTPException(status_code=401, detail='Invalid data')
    if not auth_handler.verify_password(user_details.password, user['password']):
        return HTTPException(status_code=401, detail='Check password')

    access_token = auth_handler.encode_token(user['key'])
    refresh_token = auth_handler.encode_refresh_token(user['key'])
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}


@router.post('/add_book')
def add_book(book_details: BookModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if not auth_handler.decode_token(token):
        return 'Only authorized users can add books'

    book = {'key': book_details.name, 'author': book_details.author, 'pages':book_details.pages}
    return books_db.put(book)
