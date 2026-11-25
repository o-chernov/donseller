from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix="/test")
templates = Jinja2Templates(directory="app/modules/test/templates")

router.mount("/test-static",
             StaticFiles(directory="app/modules/test/static"), name="test-static")


@router.get("")
def test(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)
