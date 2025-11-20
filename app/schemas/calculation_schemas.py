from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


class CalculationType(str, Enum):
    """Enumeration for supported calculation types"""

    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    """Schema for creating a new calculation"""

    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")
    type: CalculationType = Field(..., description="Type of calculation to perform")

    @validator("b")
    def validate_division_by_zero(cls, v, values):
        """Prevent division by zero"""
        if "type" in values and values["type"] == CalculationType.DIVIDE and v == 0:
            raise ValueError("Division by zero is not allowed")
        return v

    @validator("a", "b")
    def validate_operands(cls, v):
        """Basic validation for operands"""
        if not isinstance(v, (int, float)):
            raise ValueError("Operands must be numeric")
        return float(v)


class CalculationRead(BaseModel):
    """Schema for reading calculation data"""

    id: int
    a: float
    b: float
    type: str
    result: Optional[float]
    user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CalculationUpdate(BaseModel):
    """Schema for updating calculation data"""

    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[CalculationType] = None

    @validator("b")
    def validate_division_by_zero(cls, v, values):
        """Prevent division by zero on updates"""
        if (
            v is not None
            and "type" in values
            and values["type"] == CalculationType.DIVIDE
            and v == 0
        ):
            raise ValueError("Division by zero is not allowed")
        return v

    @validator("a", "b")
    def validate_operands(cls, v):
        """Basic validation for operands"""
        if v is not None and not isinstance(v, (int, float)):
            raise ValueError("Operands must be numeric")
        return float(v) if v is not None else v


class CalculationResponse(BaseModel):
    """Schema for calculation response with computed result"""

    id: int
    a: float
    b: float
    type: str
    result: float
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
