import json
from relayboard.testing import request
from relayboard.web import create_seeded_app
app=create_seeded_app()
def check(method,path,payload,code,expected):
    actual=request(app,method,path,payload)
    print(json.dumps({'method':method,'path':path,'input':payload,'status':actual[0],'response':actual[1]},sort_keys=True))
    assert actual[0] == code, actual
    assert actual[1] == expected, actual
job={'id':'daily-report','name':'Daily report','enabled':True,'max_attempts':2,'paused':True}
check('POST','/api/jobs/daily-report/pause',None,200,{'job':job})
check('POST','/api/jobs/daily-report/runs',{'source':'scheduled'},409,{'error':'job daily-report is paused'})
check('POST','/api/jobs/daily-report/runs',{'source':'manual'},201,{'run':{'id':'run-001','job_id':'daily-report','source':'manual','status':'running'}})
job['paused']=False
check('POST','/api/jobs/daily-report/resume',None,200,{'job':job})
check('POST','/api/jobs/daily-report/runs',{'source':'scheduled'},201,{'run':{'id':'run-002','job_id':'daily-report','source':'scheduled','status':'running'}})
print('PASS original WSGI API pause/resume and preserved manual admission')
