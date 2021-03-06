# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from flask import url_for, Blueprint, render_template
from sanic import Blueprint
from sanic_jinja2 import SanicJinja2
from jinja2 import PackageLoader

class Apidoc(Blueprint):
    '''
    Allow to know if the blueprint has already been registered
    until https://github.com/mitsuhiko/flask/pull/1301 is merged
    '''
    def __init__(self, *args, **kwargs):
        self.registered = False
        self.app = None
        super(Apidoc, self).__init__(*args, **kwargs)

    def register(self, *args, **kwargs):
        app = args[0]
        self.app = app
        super(Apidoc, self).register(*args, **kwargs)
        self.registered = True

    @property
    def config(self):
        if self.app:
            return self.app.config
        return {}

    def url_for(self, *args, **kwargs):
        return self.app.url_for(*args, **kwargs)


apidoc = Apidoc('restplus_doc', None)

loader = PackageLoader(__name__, 'templates')
j2 = SanicJinja2(apidoc, loader)


apidoc.static('/swaggerui', './sanic_restplus/static')

def swagger_static(filename):
    #url = j2.app.url_for('restplus_doc.static')
    return '/swaggerui/bower/swagger-ui/dist/{0}'.format(filename)

def config():
    return apidoc.config

j2.add_env('swagger_static', swagger_static)
j2.add_env('config', swagger_static)

# @apidoc.add_app_template_global
# def swagger_static(filename):
#     return url_for('restplus_doc.static',
#                    filename='bower/swagger-ui/dist/{0}'.format(filename))


def ui_for(request, api):
    '''Render a SwaggerUI for a given API'''
    return j2.render('swagger-ui.html', request, title=api.title,
                           specs_url=api.specs_url)
