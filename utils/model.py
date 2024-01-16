from sqlalchemy import (
    Column,
    String,
    DateTime,
    JSON,
    Float,
)
from utils.database_utils import Base


class UserActionTracking(Base):

    __tablename__ = "user_action_tracking"
    _id = Column(String, primary_key=True)
    model_name = Column(String)
    selected_api = Column(String)
    human_query = Column(String)
    graphql_query = Column(String)  
    response = Column(String)  
    generation_time = Column(Float)
    model_parameters = Column(JSON)
    miscellaneous = Column('miscellaneous', JSON) 
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            "_id": self._id,
            "model_name": self.model_name,
            "selected_api": self.selected_api,
            "human_query": self.human_query,
            "graphql_query": self.graphql_query,
            "response": self.response,
            "generation_time": self.generation_time,
            "model_parameters": self.model_parameters,
            "miscellaneous": self.miscellaneous,
            "created_at": self.created_at,
        }
