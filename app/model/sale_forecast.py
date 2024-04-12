from app import db
from app.model.forecast_detail import ForecastDetail

class SaleForecast(db.Model):
    __tablename__ = 'fact_sale_forecast'
    sale_forecast_id  = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )
    forecast_detail_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            ForecastDetail.forecast_detail_id, 
            ondelete='CASCADE'
        ),
        nullable=False
    )
    time_id = db.Column(
        db.BigInteger, 
        nullable=False
    )
    week = db.Column(
        db.Integer,
        nullable=False
    )
    week_date = db.Column(
        db.String(255),
        nullable=False
    )
    actual_total_transaction = db.Column(
        db.Float, 
        nullable=True
    )
    predict_total_transaction = db.Column(
        db.Float, 
        nullable=False
    )

    # def __repr__(self):
    #     return '<SaleForecast {}>'.format(self.name)