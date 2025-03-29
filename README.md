## FEDS Music – Flask Backend

This is the backend for the FEDS Music platform. It handles everything like authentication, music uploads, profile updates, admin control, and more.



### Tech Stack

- **Python 3.12**
- **Flask**
- **Flask-JWT-Extended**
- **MongoDB**
- **Cloudinary (external api)** (for storing music)
- **Celery (couldn't use)** (for payment processing)
- **Redis (couldn't use)** (for tasks and session-like storage)



### Setup Instructions

1. **Clone the repo:**

```bash
git clone <my-this-repo-url>
cd repo-folder
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

3. **Install requirements:**

```bash
pip install -r requirements.txt
```

4. **Set environment variables:**

Create a `.env` file and add all necessary secrets:

```
JWT_SECRET_KEY=your-secret-key
MONGODB_URL=your-mongodb-url
CLOUDINARY_API_KEY=your-key
CLOUDINARY_SECRET=your-secret
```

5. **Run the server:**

```bash
python app.py
```



### Available Routes (Main ones)

#### Authentication:
- `/user/authenticate_user`
- `/musician/authenticate_musician`
- `/admin/authenticate_admin`

#### Registration:
- `/user/add_user`
- `/musician/add_musician`
- `/admin/add_admin`

#### Profile & Music:
- `/musician/musician_profile`
- `/musician/add_music`
- `/musician/update_music`
- `/musician/update_musician_info`
- `/musician/admin_profile`
- `/musician/user_profile`

#### Forgot Password:
- `/user/update_user_info` (no JWT)
- `/musician/update_musician_info` (no JWT)
- `/admin/update_admin_info` (no JWT)



### Testing

We’re using **Pytest** to run unit tests.

To install:

```bash
pip install pytest
```

To run tests:

```bash
pytest
```

Tests are placed in the `tests/` folder.


### some Errors I Faced and How I Solved Them

#### 1. **CORS Issues**
**Problem:** When frontend called the backend, it blocked the request.
**Solution:** I added CORS support using Flask-CORS.

```python
from flask_cors import CORS
CORS(app)
```



#### 2. **422 Error when resetting password**
**Problem:** I kept getting 422 because JWT was still required.
**Solution:** I removed `@jwt_required()` from the update routes for forgot password and added this instead:

```python
data = request.json
username = data.get('user' or 'admin' or 'musician')  # depending on role
```



#### 3. **500 Internal Server Error on deleting users**
**Problem:** When I tried deleting users from the admin client page, I got a 500.
**Fix:** I forgot to pass the correct password from `search_user()` to the `delete_user()` function. I used this fix:

```python
result = search_user(admin, user_to_delete)
response, status_code = delete_user(user_to_delete, result['password'])
```



#### 4. **Issue with database connection**
**Problem:** The server kept crashing and telling me there was an iisue with connection to the database
**Solution:** I went to my mongodb and made my atlas connection accessible from any ip adress that is i made it "0.0.0.0/0"


#### 5. **Musician songs not found**
**Problem:** Admin client view said “Musician song not found” even though they existed.
**Fix:** The `/get_musician_catalogue` in utility.py was returning a dict of dict which was wrong so i made it return just the musician_detail not {musician_detail}


## API Documentation

You can view the  Swagger documentation in [docs/swagger.yaml](docs/swagger.yaml). Only the main routes i could explain because of time


### Things Left To Improve

- Protect more routes with `@jwt_required`
- Add flast rate limiter to handle amount of request
- Add user profile picture support
- Add a chatroom feature
- use celery to handle payment order


