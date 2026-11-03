"""Thin authenticated local client. Actor text never supplies credentials."""
import uuid
from .transport import request
from .encoding import Refusal


class Client:
    def __init__(self,path,actor):self.path,self.actor=path,actor
    def call(self,op,payload=None,key=None):
        return request(self.path,{'op':op,'payload':payload or {},'request_id':key or str(uuid.uuid4()),'actor':self.actor})
    def committed(self,op,payload=None,key=None):
        result=self.call(op,payload,key)
        if result.get('status')!='COMMITTED':raise Refusal(result.get('reason',result.get('status','UNKNOWN')),str(result))
        return result
    def query(self,op,payload=None):
        result=self.call(op,payload)
        if result.get('status')=='ERROR':raise Refusal(result['reason'],result.get('detail',''))
        return result
