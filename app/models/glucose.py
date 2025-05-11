from app import db
from datetime import datetime

class GlucoseReading(db.Model):
    __tablename__ = 'glucose_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    reading_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GlucoseReading {self.value} at {self.reading_time}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'value': self.value,
            'reading_time': self.reading_time.isoformat(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
