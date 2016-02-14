# email_me_when_ready

A decorator that can be wrapped around any function and will send you an email from your gmail when the function has run its course. 

In the config you have to enter your gmail username, gmail password, and a default email address that will receive the emails.

### example
```python
from email_me_when_ready import EmailMeWhenReady


@EmailMeWhenReady(recipient)
def your_function_here(*args, **kwargs):
    do stuff
    return stuff
