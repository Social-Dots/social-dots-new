# Absolute minimal WSGI app to test Vercel deployment
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [b'<h1>Social Dots</h1><p>Basic WSGI working on Vercel!</p>']

app = application