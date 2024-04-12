from app import db

class FactSale(db.Model):
    __tablename__ = 'fact_sale'
    sale_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time_id = db.Column(db.Integer)
    total_item = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    profit = db.Column(db.Integer)

    # def __repr__(self):
    #     return '<FactSale {}>'.format(self.name)