from app.main import main


@main.app_errorhandler(404)
def page_not_found():
    return 'not found current url', 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return 'server error', 500
