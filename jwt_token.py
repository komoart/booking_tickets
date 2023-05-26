from uuid import uuid4

import jwt

JWT_SECRET_KEY = 'yKSPW5h9WWqIKICI3R2O22EmCuNwSW5GdxHhkaSX2Yg9WbzAh0IswxbR1PyXK7uh'
JWT_ALGORITHM = 'HS256'

user_data = {
    'sub': str(uuid4()),
    'permissions': [0, 3],
    'is_super': False,
}
sudo_data = {
    'sub': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a',
    'permissions': [0, 3],
    'is_super': True,
}
author_data = {
    'sub': '50760ee6-2073-445d-ad25-f665937f3b33',
    'permissions': [0, 3],
    'is_super': False,
}
guest_1_data = {
    'sub': '39e60237-83ea-4c65-9bc9-f6b47d109738',
    'permissions': [0, 3],
    'is_super': False,
}
guest_2_data = {
    'sub': 'd0c5635c-3211-4cf8-94ab-cbe6800771c4',
    'permissions': [0, 3],
    'is_super': False,
}
access_token = jwt.encode(user_data, JWT_SECRET_KEY, JWT_ALGORITHM)
print('===' * 15)  # noqa: T201
print('user: ', user_data.get('sub'))  # noqa: T201
print('user_access_token: ', access_token)  # noqa: T201

access_token = jwt.encode(sudo_data, JWT_SECRET_KEY, JWT_ALGORITHM)
print('===' * 15)  # noqa: T201
print('sudo: ', sudo_data.get('sub'))  # noqa: T201
print('sudo_access_token: ', access_token)  # noqa: T201

access_token = jwt.encode(author_data, JWT_SECRET_KEY, JWT_ALGORITHM)
print('===' * 15)  # noqa: T201
print('author: ', author_data.get('sub'))  # noqa: T201
print('access_token: ', access_token)  # noqa: T201

access_token = jwt.encode(guest_1_data, JWT_SECRET_KEY, JWT_ALGORITHM)
print('===' * 15)  # noqa: T201
print('guest_1: ', guest_1_data.get('sub'))  # noqa: T201
print('access_token: ', access_token)  # noqa: T201

access_token = jwt.encode(guest_2_data, JWT_SECRET_KEY, JWT_ALGORITHM)
print('===' * 15)  # noqa: T201
print('guest_2: ', guest_2_data.get('sub'))  # noqa: T201
print('access_token: ', access_token)  # noqa: T201
