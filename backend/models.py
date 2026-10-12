from sqlalchemy import Column, Integer, String, DateTime, Text, DECIMAL, Boolean, ForeignKey, Enum, BIGINT
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    expire_date = Column(DateTime, nullable=True)
    total_usage = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TokenProduct(Base):
    __tablename__ = "token_products"
    
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    token_type = Column(String(50), unique=True, nullable=False)
    duration_hours = Column(Integer, nullable=True)
    duration_days = Column(Integer, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)
    original_price = Column(DECIMAL(10, 2), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

class TokenCard(Base):
    __tablename__ = "token_cards"
    
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    card_code = Column(String(32), unique=True, nullable=False)
    token_type = Column(String(50), ForeignKey("token_products.token_type"), nullable=False)
    duration_hours = Column(Integer, nullable=True)
    duration_days = Column(Integer, nullable=True)
    status = Column(Enum("unused", "used", "expired"), default="unused")
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=True)
    used_at = Column(DateTime, nullable=True)
    card_expire_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=False)
    mode = Column(Enum("mode1", "mode2"), nullable=False)
    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=True)
    status = Column(Enum("pending", "processing", "success", "failed"), default="pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=True)
    content = Column(Text, nullable=False)
    contact = Column(String(100), nullable=True)
    type = Column(Enum("suggestion", "bug", "complaint", "other"), default="other")
    status = Column(Enum("pending", "processed", "resolved"), default="pending")
    reply = Column(Text, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())