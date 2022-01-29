from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base


class CaribbeanJobsPost(Base):
    __tablename__ = "caribbeanjobs_posts"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String,nullable=False)
    caribbeanjobs_job_id = Column(Integer, unique=True,nullable=True)
    job_title = Column(String,nullable=False)
    job_company = Column(String,nullable=False)
    job_category = Column(String,nullable=True)
    job_location = Column(String,nullable=True)
    job_salary = Column(String,nullable=True)
    job_min_education_requirement = Column(String,nullable=True)
    full_job_description = Column(String,nullable=True)
    job_listing_date = Column(Date,default=datetime.now().date(),nullable=False)
    job_delisting_date = Column(Date,nullable=True)
    job_listing_is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")
