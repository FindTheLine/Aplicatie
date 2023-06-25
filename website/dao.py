from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from . import db
import inspect

def get_required_parameters(Table:object, criteria:dict) -> dict:
    parameters = inspect.signature(Table.__init__).parameters
    required_params = dict([(k,v) for k,v in criteria.items() if k in parameters.keys()])   
    
    return required_params

class DAO:
    def __init__(self):
        self.session = db.session

    def get_session(self):
        return self.session

    def commit_changes(self):
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def close_session(self):
        self.session.close()

class TableDAO(DAO):
    def get_rows_excluded_ids(self,Table, excluded_ids:list[int]=[]):
        return self.session.query(Table).filter(~Table.id.in_(excluded_ids)).all()
    
    def get_query_by_criteria(self, Table:object, criteria:dict={}):
        required_params = get_required_parameters(Table, criteria)
        query = self.session.query(Table)
        for key, value in required_params.items():
            if value is not None:
                query = query.filter(getattr(Table, key) == value)
                
        return query
    
    def get_row_by_criteria(self, Table:object, criteria:dict={}, descending=False) -> object:
        query = self.get_query_by_criteria(Table,criteria)
        
        if descending:
            return query.order_by(Table.id.desc()).first()
        return query.first()

    
    def get_rows_by_criteria(self,Table, criteria:dict={}, descending=False):
        query = self.get_query_by_criteria(Table,criteria)
                
        if descending:
            return query.order_by(Table.id.desc()).all()
        return query.all()
    
