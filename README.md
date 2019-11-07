# A Flask Web Api Demo

---

## *Feature:*
- ### Validate request params
- ### Auto add swagger doc

---

## *Usage:*
###*Step 1:* add validator for api request params
```python
class AddUserValidator(BaseValidator):
    name = StringField(max_length=20, min_length=1, desc="user name", required=True)
    age = IntegerField(minimum=1, maximum=100, desc="user age")
    sex = EnumField(enums=["man", "woman"], default="man", desc="user sex")
    url = UrlField(max_length=256, desc="user blog url", default="https://www.json.cn/")
```
###*Step 2:* write your api
```python
@user_bp.route('/add_user', methods=['GET', 'POST'])
@validate_params(validator=AddUserValidator)
def add_user(**request_params):
    """
    Add a new user
    :param request_params:
    :return:
    """
    pass
```
###*Step 3:* start you api and visit your swagger api --> /api/doc, you can config it in config.py

---

## *Todo:*
- ### scheduler
- ### db manager
