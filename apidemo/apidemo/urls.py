"""
URL configuration for apidemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from ninja.renderers import BaseRenderer
from django.http import Http404


class HTMLRenderer(BaseRenderer):
    media_type = "text/html"

    def render(self, request, data, response_status):
        return data


# api = NinjaAPI()
api = NinjaAPI(renderer=HTMLRenderer())


class HelloSchema(Schema):
    name: str = "world"


@api.exception_handler(Http404)
def page_not_found(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=404,
    )


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.exception_handler(Http404)
def not_found_handler(request, exc):
    print(exc)
    return api.create_response(
        request,
        {"detail": "Not found erik"},
        status_code=404
    )


@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"


@api.get("/hello_html")
def hello_html(request, name):
    return f"<h1>Hello {name}</h1>"


@api.post("/hello_schema")
def hello_schema(request, data: HelloSchema):
    """
    Input a name into the hello_schema api and it will greet that name
    """
    return f"Hello {data.name}"


@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


@api.get("/math_another_way/{a}and{b}")
def math_another_way(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


@api.exception_handler(Http404)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "Object not found"},
        status=404,
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
