from . import db, datetime
from .models import Eval
from .dao import TableDAO, get_required_parameters
from sqlalchemy import and_, cast,Float, func
from dataclasses import dataclass, field
from statistics import mean,median,mode,fmean 
import inspect
from re import search


dao = TableDAO()

@dataclass(slots=True)
class Scores:    
    eval: object = field(default_factory=object)
    scores: list[int] = field(default_factory=list, init=False)
    criteria_1: list[int] = field(default_factory=list, init=False)
    criteria_2: list[int] = field(default_factory=list, init=False)
    criteria_3: list[int] = field(default_factory=list, init=False)
    criteria_4: list[int] = field(default_factory=list, init=False)
    date: datetime = field(default_factory=datetime, init=False)
    
    def __init__(self, eval):        
        self.scores = _eval_scores(eval)
        self.criteria_1 = [int(score) for score in self.scores[0:10]]
        self.criteria_2 = [int(score) for score in self.scores[10:15]]              
        self.criteria_3 = [int(score) for score in self.scores[15:21]]    
        self.criteria_4 = [int(score) for score in self.scores[21:24]]
        self.date = eval.creation_date
        
    def get_averages(self, average_func) -> dict:    
        averages:dict = {
            "0":str(average_func(self.scores)),
            "1":str(average_func(self.criteria_1)),
            "2":str(average_func(self.criteria_2)),
            "3":str(average_func(self.criteria_3)),
            "4":str(average_func(self.criteria_4))
        }    
        
        return averages

    def get_label_averages(self, average_func) -> dict:        
        averages:dict = self.get_averages(average_func)
        averages["label"] = self.date.strftime('%d.%m.%Y')

        return averages


class SingleAverages:
    def __init__(self) -> None:
        self.average_func = fmean
    
    def set_func(self, average_func):
        self.average_func = average_func
    
    def set_averages(self,filters:dict, start:datetime=datetime(1900,1,1), end:datetime=datetime.today()):
        evals:list = dao.get_rows_by_criteria(Eval, filters)
        result = _empty_result()

        for eval in evals:
            if eval.interval(start, end):
                scores:object = Scores(eval)
                
                eval_averages:dict = scores.get_averages(mean)
                
                for k,v in result.items():
                    if v:
                        result[k] = f"{result[k]},{eval_averages[k]}"
                    else:
                        result[k] = eval_averages[k]
        
        self.averages = result
        
    def get_averages(self):
        return self.averages

    def _calculate(self,averages):
        result = self.average_func(list(map(lambda x:float(x),averages)))
            
        return result

    def calculate(self, ordered=False):
        result = {}
        for k,v in self.averages.items():
            values = v.split(",")
            if ordered:
                result[k] = self._calculate(sorted(values))
            else:
                result[k] = self._calculate(values)

        return result
    
    def calculate_crit_label_averages(self,ordered=False):
        if ordered:
            result = self.calculate(ordered=True)
        else:
            result = self.calculate()
        result['label'] = "Toate,C1,C2,C3,C4"   

        return result


class MultiAverages(SingleAverages):
    def set_averages(self,filters:dict, start:datetime=datetime(1900,1,1), end:datetime=datetime.today()):
        evals:list = dao.get_rows_by_criteria(Eval, filters)
        
        result = _empty_label_result()
                
        for eval in evals:
            if eval.interval(start, end):
                scores:object = Scores(eval)
                
                eval_averages:dict = scores.get_label_averages(mean)
                
                for k,v in result.items():
                    if v:
                        result[k] = f"{result[k]},{eval_averages[k]}"
                    else:
                        result[k] = eval_averages[k]
                
        self.averages:dict = result
            

def _eval_scores(eval:object):
    columns = [i for i in inspect.getmembers(eval)
               if i[0].startswith('row_')]

    scores = [i[1] for i in sorted(columns, key=lambda x: int(search(r'\d+', x[0]).group()))]

    return scores

def averages_items_list(*args) -> list:
    return list(args)

def _empty_result():
    result:dict = {
        "0":"",
        "1":"", 
        "2":"",
        "3":"", 
        "4":"",
    }
    
    return result

def _empty_label_result():
    result = _empty_result()
    result["label"] = ""
    
    return result
