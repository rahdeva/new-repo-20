from app import db

class DimTime(db.Model):
    __tablename__ = 'dim_time'
    time_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    month_name = db.Column(db.String(20))
    quarter = db.Column(db.String(2))
    year = db.Column(db.Integer)

    # def __repr__(self):
    #     return '<DimTime {}>'.format(self.name)