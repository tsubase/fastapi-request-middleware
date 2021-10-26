import uvicorn
from fastapi import FastAPI, Query, Request
from typing import Optional

app = FastAPI()


@app.middleware("http")
async def check_query_string(request: Request, call_next):

    if request.method == 'GET':
        s = request.scope['query_string'].decode().split('&')
        not_none_list = [i for i in s if i.split('=')[-1] != '']
        new_query_string = '&'.join(not_none_list)
        request.scope['query_string'] = bytes(new_query_string, encoding='utf-8')

    response = await call_next(request)
    return response


@app.get('/all')
def get_all(
    min: Optional[int] = Query(None),
    max: Optional[int] = Query(None),
    skip: Optional[int] = Query(None),
    limit: Optional[int] = Query(None),
):
    print(min, max, skip, limit)
    return []



if __name__=='__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=4)