
def do_work(operation, n1, n2):
    f1 = float(n1)
    f2 = float(n2)
    if operation == 'add':
        result = f1 + f2
        conjunction = 'plus'
    elif operation == 'subtract':
        result = f1 - f2
        conjunction = 'minus'
    elif operation == 'multiply':
        result = f1 * f2
        conjunction = 'times'
    elif operation == 'divide':
        try:
            result = f1 / f2
            conjunction = 'divided by'
        except ZeroDivisionError:
            raise ZeroDivisionError
    else:
        raise NameError

    body = '<h1>{} {} {} = {}</h1>'.format(n1, conjunction, n2, result)
    return  body


def resolve_path(path):
    operations = ['add','subtract','multiply','divide']

    try:
        operation, n1, n2 = path.lstrip('/').split('/')
    except:
        raise NameError

    if operation not in operations:
        raise NameError

    return operation, n1, n2


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        operation, n1, n2 = resolve_path(path)
        body = do_work(operation, n1, n2)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 Divide By Zero"
        body = "<h1>Divide By Zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

