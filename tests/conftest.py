import os
import sys

import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def test_db():
    """Fixture for test database setup"""
    from app.database import Base, test_engine

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(test_db):
    """Fixture for database session"""
    from app.database import TestingSessionLocal

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_calculation_data():
    """Fixture providing sample calculation data"""
    return {"a": 10.0, "b": 5.0, "type": "Add", "result": 15.0}


@pytest.fixture
def test_user(db_session):
    """Create a test user for calculations"""
    from app.models.user_model import User

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password_here",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def multiple_calculations():
    """Sample calculation data for batch testing"""
    return [
        {"a": 10.0, "b": 5.0, "type": "Add", "expected": 15.0},
        {"a": 20.0, "b": 8.0, "type": "Sub", "expected": 12.0},
        {"a": 6.0, "b": 7.0, "type": "Multiply", "expected": 42.0},
        {"a": 15.0, "b": 3.0, "type": "Divide", "expected": 5.0},
    ]
