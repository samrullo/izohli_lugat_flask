from application import db
import json

class IzohliLugat(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    cyr=db.Column(db.String(200))
    cyr_def=db.Column(db.Text)
    latin=db.Column(db.String(200))
    latin_def=db.Column(db.Text)

    @classmethod
    def from_dict(cls, data):
        return cls(cyr=data['cyr'],cyr_def=data['cyr_def'],latin=data['latin'],latin_def=data['latin_def'])
    
    def as_dict(self):
        return {"id":self.id,"cyr":self.cyr,"cyr_def":self.cyr_def,"latin":self.latin,"latin_def":self.latin_def}