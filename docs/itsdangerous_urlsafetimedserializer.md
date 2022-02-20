# How URLSafeTimedSerializer works
- Import URLSafeTimedSerializer from itsdangerous
- Initialize Serializer with secret key and optional salt
- generate token from data
- When decoding data back from the token you can pass expiration time in seconds to max_age argument

```python
from itsdangerous import URLSafeTimedSerializer
s=URLSafeTimedSerializer("secret")
token=s.dumps({"id":1,"username":"samrullo"})
data=s.loads(token,max_age=60*60)
```