# Calculation API

A robust FastAPI application for mathematical calculations with user management, built with SQLAlchemy and comprehensive testing.

## Features

- **Mathematical Operations**: Support for addition, subtraction, multiplication, and division
- **User Management**: User registration and calculation history tracking
- **Factory Pattern**: Extensible calculation operations using the factory design pattern
- **Data Validation**: Comprehensive input validation with Pydantic schemas
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Comprehensive Testing**: Unit and integration tests with 80%+ code coverage
- **CI/CD Pipeline**: Automated testing and Docker deployment via GitHub Actions

## Technology Stack

- **Backend**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.4.2
- **Migrations**: Alembic 1.13.1
- **Testing**: Pytest with coverage reporting
- **Containerization**: Docker with multi-stage builds
- **CI/CD**: GitHub Actions with PostgreSQL service container

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd calculation-api
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build and run with Docker**
   ```bash
   docker build -t calculation-app .
   docker run -p 8000:8000 -e DATABASE_URL="your-db-url" calculation-app
   ```

2. **Using Docker Compose** (recommended for development)
   ```bash
   docker-compose up -d
   ```

## API Documentation

Once the application is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## Testing

### Run All Tests
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_calculation_factory.py tests/test_calculation_schemas.py -v

# Integration tests only  
pytest tests/test_calculation_integration.py -v

# With coverage reporting
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80
```

### Test Database Setup
Tests use SQLite by default for isolation. For PostgreSQL integration testing:

```bash
# Set up test database
export TEST_DATABASE_URL="postgresql://testuser:testpass@localhost/testdb"
pytest tests/test_calculation_integration.py -v
```

## Architecture

### Models
- **User**: User management with authentication support
- **Calculation**: Mathematical operations with audit trails

### Schemas
- **CalculationCreate**: Input validation for new calculations
- **CalculationRead**: Serialization for API responses  
- **CalculationUpdate**: Partial update validation

### Services
- **CalculationFactory**: Factory pattern for operation extensibility
- Individual operation classes: `AddOperation`, `SubOperation`, `MultiplyOperation`, `DivideOperation`

### Database Design
```sql
-- Users table
users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Calculations table
calculations (
    id SERIAL PRIMARY KEY,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL,
    type VARCHAR(20) NOT NULL,
    result FLOAT,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow:

### Automated Testing
- **Linting**: Code quality checks with flake8, black, and isort
- **Unit Tests**: Factory pattern and schema validation tests
- **Integration Tests**: Database operations and model relationships
- **Coverage**: Minimum 80% code coverage requirement
- **Security**: Bandit security scanning and dependency safety checks

### Docker Deployment
- **Automated Builds**: Docker images built on every push to main
- **Docker Hub**: Images pushed to Docker Hub registry
- **Multi-arch Support**: Built for multiple platforms
- **Security**: Non-root user and minimal attack surface

### Pipeline Stages
1. **Code Quality**: Linting and formatting checks
2. **Testing**: Unit and integration tests with PostgreSQL
3. **Security**: Vulnerability scanning
4. **Build**: Docker image creation and testing
5. **Deploy**: Push to Docker Hub (main branch only)

## Docker Hub Repository

The application is automatically deployed to Docker Hub:
- **Latest**: `yourusername/calculation-app:latest`
- **Tagged**: `yourusername/calculation-app:<commit-sha>`

### Pull and Run
```bash
docker pull yourusername/calculation-app:latest
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host/db" \
  yourusername/calculation-app:latest
```

## Development Guidelines

### Adding New Operations
1. Create operation class implementing `CalculationOperation` protocol
2. Register in `CalculationFactory._operations`
3. Add to `CalculationType` enum
4. Write comprehensive tests
5. Update documentation

### Database Changes
1. Modify models in `app/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review and edit migration file
4. Apply: `alembic upgrade head`
5. Update tests accordingly

### Testing Standards
- Maintain 80%+ code coverage
- Write both unit and integration tests
- Test error conditions and edge cases
- Use meaningful test descriptions
- Mock external dependencies appropriately

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Production database connection string | `sqlite:///./calculation_app.db` |
| `TEST_DATABASE_URL` | Test database connection string | `sqlite:///./test_calculation_app.db` |
| `SECRET_KEY` | JWT secret key for authentication | Required for production |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `pytest tests/ -v`
5. Commit with conventional commits: `git commit -m "feat: add new operation"`
6. Push and create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review test examples for usage patterns