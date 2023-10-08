from starlette.requests import Request
async def pprint_request(request: Request,html=True):
    body = await request.body()
    print(body)
    pprint_request='{}\n{}\r\n{}\r\n\r\n{}'.format(
                '-----------START-----------',
                request.method + ' ' + request.url.path,
                '\r\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
                str(body, encoding='utf-8'),
            )
    if html:
        response =  "<h2>Request</h2>"
        response += "<div><textarea style='height:25em;width:80%;margin:auto;'>"
        response +=  pprint_request
        response += "</textarea></p></div>"
        return response
    return pprint_request
