import json
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, TEXT

from src.database import Base
from src.inbounds.schemas import (
    InboundSecurity,
    InboundType,
    InboundFingerPrint,
    InboundNetwork,
)


class JSONList(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


class InboundConfig(Base):
    __tablename__ = "inbound_config"

    id = Column(Integer, primary_key=True, index=True)
    inbound_id = Column(Integer, ForeignKey("inbound.id"), nullable=True)
    inbound = relationship("Inbound", back_populates="inbound_configs")
    remark = Column(String(128), index=True)
    port = Column(Integer, index=True)
    domain = Column(String(128), index=True)
    host = Column(String(128), index=True)
    sni = Column(String(128), index=True)
    address = Column(String(128), index=True)
    path = Column(String(400))
    pbk = Column(String(400))
    sid = Column(String(400))
    spx = Column(String(400))
    enable = Column(Boolean, default=True)
    develop = Column(Boolean, default=False)

    finger_print = Column(
        Enum(InboundFingerPrint),
        unique=False,
        nullable=False,
        default=InboundFingerPrint.default.value,
    )

    security = Column(
        Enum(InboundSecurity),
        unique=False,
        nullable=False,
        default=InboundSecurity.default.value,
    )

    network = Column(
        Enum(InboundNetwork),
        unique=False,
        nullable=False,
        default=InboundNetwork.ws.value,
    )

    alpns = Column(JSONList)

    type = Column(Enum(InboundType), nullable=False, default=InboundType.default.value)
    config_mode = Column(
        String(128), nullable=False, default="auto"
    )  # Renamed from 'mode' to 'config_mode'
    extra = Column(String(2048), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
