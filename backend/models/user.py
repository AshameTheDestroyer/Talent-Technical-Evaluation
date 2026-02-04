from sqlalchemy import Column, String, CheckConstraint
from .base import Base
import uuid
from utils.password_utils import get_password_hash, verify_password
import re

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'hr' or 'applicant'

    # Add constraint to ensure role is either 'hr' or 'applicant'
    __table_args__ = (CheckConstraint(role.in_(['hr', 'applicant']), name='valid_role'),)

    def set_password(self, password: str):
        """Hash and set the user's password"""
        self.password = get_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash"""
        return verify_password(password, self.password)

    def validate_name(self, name: str) -> bool:
        """Validate that the name contains only letters, spaces, hyphens, and apostrophes"""
        if not name:
            return False
        # Allow letters, spaces, hyphens, and apostrophes, with length between 1 and 50
        pattern = r"^[a-zA-Z\s\-']{1,50}$"
        return bool(re.match(pattern, name.strip()))

    def validate_first_name(self) -> bool:
        """Validate the first name"""
        return self.validate_name(self.first_name)

    def validate_last_name(self) -> bool:
        """Validate the last name"""
        return self.validate_name(self.last_name)