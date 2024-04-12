from app import db

class ForecastDetail(db.Model):
    __tablename__ = 'dim_forecast_detail'
    forecast_detail_id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )
    method = db.Column(
        db.String(255), 
        nullable=False
    )
    last_week_date = db.Column(
        db.String(255), 
        nullable=False
    )
    last_week_transaction = db.Column(
        db.Float, 
        nullable=False
    )
    mae = db.Column(
        db.Float, 
        nullable=False
    )
    mse = db.Column(
        db.Float, 
        nullable=False
    )
    rsme = db.Column(
        db.Float, 
        nullable=False
    )

    # def __repr__(self):
    #     return '<ForecastDetail {}>'.format(self.name)
