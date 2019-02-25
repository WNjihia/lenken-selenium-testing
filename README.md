### Lenken Selenium Testing

This is an e2e test example for requesting mentorship via [lenken](lenken.andela.com). These tests are written using [selenium](https://selenium-python.readthedocs.io/)

http://recordit.co/okqlX5k5OP

### Installation and Setup

Clone the repository from GitHub:
```
$ git clone https://github.com/WNjihia/lenken-selenium-testing.git
```

Navigate to the `lenken-selenium-testing` directory:
```
$ cd lenken-selenium-testing
```

Create a virtual environment:
> Use [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to create and activate a virtual environment.

Install the required packages:
```
$ pip install -r requirements.txt

```

Install the chrome driver:
> Download the chrome browser driver [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure it's in your PATH

Run the tests:
```
$ python test_request.py
```
