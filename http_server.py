import socket
import sys
import traceback
import mimetypes
import os

def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->

        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """
    resp = b"HTTP/1.1 200 OK\r\n"
    resp += b"Content-Type: "
    resp += mimetype
    resp += b"\r\n"
    resp += b"\r\n"
    resp += body
    print(resp)

    # TODO: Implement response_ok
    return resp

def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # TODO: Implement response_method_not_allowed
    # return b""
    resp = "HTTP/1.1 405 Method Not Allowed\r\n"
    resp += "Content-Type: text/plain\r\n"
    resp += "\r\n"
    resp += "<b>405 Method Not Allowed</b>"
    resp += "\r\n"
    return resp.encode()


def response_not_found(path=None):
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found
    resp = "HTTP/1.1 404 Not Found\r\n"
    resp += "Content-Type: text/html\r\n"
    resp += "\r\n"
    resp += "<b>{} - 404 not found</b>".format(path)
    return resp.encode()


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # TODO: implement parse_request
    # print(type(request))
    req_lines = request.splitlines()
    # inc = 0

    for line in req_lines:
        # inc += 1
        # print(f"{inc}: {line}")
        if "GET" in line:
            path = line.split()[1]
            break
    else:
        raise NotImplementedError(f"This server only handles GET requests")

    return path
    # return ""

def response_path(path):
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """
    sys_dir = os.getcwd()
    path = "." + path
    path = path.replace("." + os.sep, "." + os.sep + "webroot" + os.sep)
    # path = sys_dir + path
    # print(f"{path}, {os.path.isdir(path)}")
    # if path == path.replace("." + os.sep, "." + os.sep + "webroot" + os.sep):
    #     path = path + "webroot"
        # print(f"going to {path}")

    if os.path.isdir(path):
        # print(f"{path} is a dir")
        list_dir = os.listdir(path)

        mime_type = b"text/plain"
        content = ""
        for line in list_dir:
            content += line
            content += "\r\n"
        return content.encode(), mime_type
    elif os.path.isfile(path):
        file_type = mimetypes.guess_type(path)[0]
    else:
        path = sys_dir + path
        # return response_not_found(path)
        raise NameError(path)
    # html
    if file_type == 'text/html':
        mime_type = b"text/html"
        content = ""
        with open(path, 'r') as fh:
            for line in fh:
                content += line
        return content.encode(), mime_type
    # text
    if file_type == 'text/plain':
        # print(f"{path} is text")
        mime_type = b"text/plain"
        content = ""
        with open(path, 'r') as fh:
            for line in fh:
                content += line
        return content.encode(), mime_type
    # icon
    if file_type == 'image/vnd.microsoft.icon':
        # print(f"{path} is microsoft icon image")
        mime_type = b"image/vnd.microsoft.icon"
        content = b""
        with open(path, 'rb') as fh:
            buff = fh.read(1024)
            while buff:
                content += buff
                buff = fh.read(1024)
        return content, mime_type

    # python
    if file_type == 'text/x-python':
        # print(f"{path} is python file")
        # mime = b"text/x-python"
        mime_type = b"text/plain"
        content = ""
        with open(path, 'r') as fh:
            for line in fh:
                content += line
        return content.encode(), mime_type
        # TODO execute python script instead
        # TODO properly handle mime = b"text/x-python"

    # png
    if file_type == 'image/png':
        # print(f"{path} is png image file")
        mime_type = b"image/png"
        content = b""
        with open(path, 'rb') as fh:
            buff = fh.read(1024)
            while buff:
                content += buff
                buff = fh.read(1024)
        return content, mime_type

    # jpeg
    if file_type == 'image/jpeg':
        # print(f"{path} is jpeg image file")
        mime_type = b"image/jpeg"
        content = b""
        with open(path, 'rb') as fh:
            buff = fh.read(1024)
            while buff:
                content += buff
                buff = fh.read(1024)
        return content, mime_type



    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.
    
    content = b"not implemented"
    mime_type = b"not implemented"

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break
		

                print("Request received:\n{}\n\n".format(request))

                # TODO: Use parse_request to retrieve the path from the request.
                try:
                    path = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        response = response_ok(body=response_path(path)[0],
                                               mimetype=response_path(path)[1])
                    except NameError as e:
                        response = response_not_found(str(e))

                # print(f"path: {path}")


                # TODO: Use response_path to retrieve the content and the mimetype,
                # based on the request path.

                # to_send = response_path(path)
          
                # conn.sendall(to_send)


                # TODO; If parse_request raised a NotImplementedError, then let
                # response be a method_not_allowed response. If response_path raised
                # a NameError, then let response be a not_found response. Else,
                # use the content and mimetype from response_path to build a 
                # response_ok.
                
                
                # response = response_ok(
                #     body=b"Welcome to my web server",
                #     mimetype=b"text/plain"
                # )

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)


