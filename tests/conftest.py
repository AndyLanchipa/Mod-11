import pytest
import os
import sys

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
    return {
        "a": 10.0,
        "b": 5.0,
        "type": "Add",
        "result": 15.0
    }
