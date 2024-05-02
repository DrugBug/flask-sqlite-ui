import uuid
from enum import Enum

from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from app import db

TRACKING_NUMBER_LENGTH = 6


class PackageType(Enum):
    LETTER = "Letter"
    PACKAGE = "Package"


class PostOffice(db.Model):
    __tablename__ = "post_offices"

    address = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False, primary_key=True)

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "zip_code": self.zip_code
        }


class Package(db.Model):
    __tablename__ = "packages"

    @staticmethod
    def _generate_tracking_number():
        return str(uuid.uuid4()).replace("-", "")[:TRACKING_NUMBER_LENGTH]

    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    destination_address = db.Column(db.String(200), nullable=False)
    destination_zip_code = db.Column(db.String(10), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    tracking_number = db.Column(db.String(TRACKING_NUMBER_LENGTH), primary_key=True, default=_generate_tracking_number)
    package_type = db.Column(db.Enum(PackageType))
    delivered = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "tracking_number": self.tracking_number,
            "destination_address": self.destination_address,
            "destination_zip_code": self.destination_zip_code,
            "recipient_name": self.recipient_name,
            "package_type": self.package_type.value,
            "delivered": self.delivered
        }


class PackageTrackingHistory(db.Model):
    __tablename__ = "packages_tracking_history"

    package_id = db.Column(db.String, db.ForeignKey('packages.tracking_number'), primary_key=True)
    package = db.relationship("Package", backref=backref("tracking"))
    route = db.Column(db.String(2000), nullable=False, default="")  # Example: "" (empty), "NY Post" (1), "NY Post->LA Post" (2)

    def to_dict(self):
        return {
            "package": self.package_id,
            "route": self.route,
            "delivered": self.package.delivered
        }
