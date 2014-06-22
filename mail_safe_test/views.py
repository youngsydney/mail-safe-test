"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from flask import request, flash, url_for, redirect
from flask import Flask, render_template, request, make_response
from authomatic.adapters import WerkzeugAdapter
from mail_safe_test import app

def login(provider_name):
    print("LOGIN")
    response = make_response()
    result = app.authomatic.login(WerkzeugAdapter(request, response), provider_name)

    if result:
        if result.user:
            result.user.update()
        return "success" #render_template('login.html', result=result)
    else:
        return "failure"
