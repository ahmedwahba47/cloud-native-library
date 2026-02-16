# Cloud-Native Library Management System

A distributed microservices system built with **Spring Boot 3.2** and **Spring Cloud 2023.0.4**, demonstrating cloud-native architecture patterns including service discovery, centralized configuration, API gateway with JWT authentication, resilience patterns, and distributed tracing.

**Student:** Ahmed Wahba (A00336722)
**Module:** Microservices Architecture

---

## Architecture Overview

```
                         +------------------+
                         |   API Gateway    |
                         |    (port 8080)   |
                         |   JWT Auth +     |
                         |   Routing        |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
           +-------v--------+         +--------v--------+
           | Catalog Service |         |  Library API    |
           |   (port 8082)   |-------->|   (port 8081)   |
           | Reading Lists & |  Feign  | Books & Loans   |
           | Recommendations |  Client | CRUD Operations |
           +----------------+         +-----------------+
                    |                           |
                    v                           v
               H2 Database                 H2 / PostgreSQL

   +------------------+    +------------------+    +------------------+
   |  Eureka Server   |    |  Config Server   |    |     Zipkin       |
   | Service Discovery|    | Centralized Conf |    | Distributed      |
   |   (port 8761)    |    |   (port 8888)    |    | Tracing (9411)   |
   +------------------+    +------------------+    +------------------+
```

All services register with **Eureka** for dynamic discovery. The **Config Server** provides externalized configuration. **Zipkin** collects distributed traces via Micrometer.

---

## Services

### 1. Eureka Server (Service Discovery)
- **Port:** 8761
- **Purpose:** Netflix Eureka-based service registry enabling dynamic service discovery
- **Dashboard:** `http://localhost:8761`
- All microservices register on startup and discover each other by service name

### 2. Config Server (Centralized Configuration)
- **Port:** 8888
- **Purpose:** Spring Cloud Config Server providing externalized configuration for all services
- **Backend:** Native file-based (configurations stored in `configurations/` directory)
- **Profiles:** Per-service YAML files (`library-api.yml`, `catalog-service.yml`, `api-gateway.yml`)

### 3. API Gateway
- **Port:** 8080
- **Purpose:** Single entry point for all client requests
- **Features:**
  - Route definitions using Eureka service discovery (`lb://` URIs)
  - JWT authentication filter (global)
  - Token generation endpoint (`POST /auth/token`)
  - Public endpoints whitelisted (Eureka, actuator, auth)
- **Technology:** Spring Cloud Gateway, JJWT 0.12.6

### 4. Library API (Service B - Core Service)
- **Port:** 8081
- **Purpose:** Core REST API managing books and loans with full CRUD operations
- **Features:**
  - Book management (create, read, update, delete, search)
  - Loan management with available copies tracking
  - DTO pattern with MapStruct-style manual mappers
  - Pagination and sorting support
  - Jakarta Bean Validation
  - Standardized error responses
- **Database:** H2 (dev), PostgreSQL (prod)
- **Testing:** 58 unit tests (Mockito) + 60 integration tests (MockMvc + H2) = 118 total
- **CI/CD:** Jenkinsfile with 9-stage pipeline, SonarQube quality gate, JaCoCo coverage

### 5. Catalog Service (Service A - Dependent Service)
- **Port:** 8082
- **Purpose:** Manages reading lists and book recommendations, depends on Library API
- **Features:**
  - Reading list creation and management
  - Book recommendations with categories and difficulty levels
  - Enriches responses with book details from Library API
- **Integration:** OpenFeign declarative HTTP client to Library API
- **Resilience:**
  - Resilience4j circuit breaker (failure threshold: 50%, wait duration: 30s)
  - Retry with exponential backoff (max 3 attempts)
  - Fallback responses when Library API is unavailable
- **Database:** H2

---

## Cloud-Native Patterns Demonstrated

| Pattern | Implementation | Purpose |
|---------|---------------|---------|
| Service Discovery | Netflix Eureka | Dynamic service registration and lookup |
| Centralized Configuration | Spring Cloud Config | Externalized config, environment-specific profiles |
| API Gateway | Spring Cloud Gateway | Single entry point, routing, cross-cutting concerns |
| Circuit Breaker | Resilience4j | Fault isolation, prevent cascade failures |
| Retry | Resilience4j | Transient failure recovery with exponential backoff |
| Fallback | Feign + Resilience4j | Graceful degradation when dependencies are down |
| Distributed Tracing | Micrometer + Zipkin | Request correlation across service boundaries |
| JWT Authentication | Spring Security + JJWT | Stateless authentication at the gateway |
| Containerization | Docker + Compose | Consistent deployment across environments |

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Java | 21 |
| Framework | Spring Boot | 3.2.0 |
| Cloud | Spring Cloud | 2023.0.4 |
| Service Discovery | Netflix Eureka | - |
| Configuration | Spring Cloud Config | - |
| Gateway | Spring Cloud Gateway | - |
| HTTP Client | OpenFeign | - |
| Resilience | Resilience4j | 2.2.0 |
| Tracing | Micrometer + Brave + Zipkin | - |
| Authentication | JJWT | 0.12.6 |
| Database | H2 (dev) / PostgreSQL (prod) | - |
| Testing | JUnit 5 + Mockito + Spring Test | - |
| Coverage | JaCoCo | - |
| Build | Maven | 3.9.x |
| Containers | Docker + Docker Compose | - |
| CI/CD | Jenkins | - |
| Code Quality | SonarQube | - |

---

## Getting Started

### Prerequisites

- Java 21+
- Maven 3.9+
- Docker & Docker Compose (for containerized deployment)

### Option 1: Docker Compose (Recommended)

Start all services with a single command:

```bash
docker-compose up --build
```

This starts all 6 services in the correct order with health checks and dependency management.

### Option 2: Run Individually

Start services in this order (each in a separate terminal):

```bash
# 1. Service Discovery
cd eureka-server && ./mvnw spring-boot:run

# 2. Configuration Server
cd config-server && ./mvnw spring-boot:run

# 3. Core Library API
cd library-api && ./mvnw spring-boot:run

# 4. Catalog Service
cd catalog-service && ./mvnw spring-boot:run

# 5. API Gateway
cd api-gateway && ./mvnw spring-boot:run
```

Optionally start Zipkin for tracing:
```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

---

## API Usage

### Authentication

```bash
# Generate JWT token
curl -X POST http://localhost:8080/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

### Library API (via Gateway)

```bash
# Get all books
curl http://localhost:8080/api/books \
  -H "Authorization: Bearer <token>"

# Create a book
curl -X POST http://localhost:8080/api/books \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "9780132350884",
    "availableCopies": 5
  }'

# Search books
curl "http://localhost:8080/api/books/search?keyword=clean" \
  -H "Authorization: Bearer <token>"
```

### Catalog Service (via Gateway)

```bash
# Create a reading list
curl -X POST http://localhost:8080/api/reading-lists \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Software Engineering Essentials",
    "description": "Must-read books for developers"
  }'

# Add a book to reading list
curl -X POST http://localhost:8080/api/reading-lists/1/books \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"bookId": 1}'

# Create a recommendation
curl -X POST http://localhost:8080/api/recommendations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "bookId": 1,
    "category": "SOFTWARE_ENGINEERING",
    "difficulty": "INTERMEDIATE",
    "reason": "Foundational text on writing maintainable code"
  }'
```

---

## Resilience Demo

### Circuit Breaker in Action

1. Start all services normally and verify Catalog Service works
2. Stop Library API: `docker-compose stop library-api`
3. Call Catalog Service — circuit breaker opens, fallback responses returned
4. Restart Library API: `docker-compose start library-api`
5. After 30 seconds, circuit transitions to half-open, then closes when calls succeed

### Circuit Breaker States

```
CLOSED (normal) --[50% failures]--> OPEN (fail fast, fallback)
                                       |
                                  [30s wait]
                                       |
                                    HALF-OPEN
                                   /        \
                          [success]          [failure]
                              |                 |
                           CLOSED             OPEN
```

---

## Observability

### Distributed Tracing (Zipkin)

- **Dashboard:** `http://localhost:9411`
- All services propagate trace IDs via Micrometer + Brave
- View end-to-end request traces across service boundaries
- Identify latency bottlenecks and failure points

### Health Endpoints

Each service exposes Spring Boot Actuator health endpoints:

| Service | Health URL |
|---------|-----------|
| Eureka Server | `http://localhost:8761/actuator/health` |
| Config Server | `http://localhost:8888/actuator/health` |
| API Gateway | `http://localhost:8080/actuator/health` |
| Library API | `http://localhost:8081/actuator/health` |
| Catalog Service | `http://localhost:8082/actuator/health` |

---

## Testing

Library API includes a comprehensive test suite:

```bash
cd library-api

# Run unit tests only (58 tests, ~3 seconds)
./mvnw test

# Run all tests including integration (118 tests)
./mvnw verify

# Generate coverage report
./mvnw verify jacoco:report
# Report at: target/site/jacoco/index.html
```

### Test Distribution

| Type | Count | Framework | Scope |
|------|-------|-----------|-------|
| Unit Tests | 58 | JUnit 5 + Mockito | Service layer isolation |
| Integration Tests | 60 | Spring MockMvc + H2 | Full HTTP endpoint testing |
| **Total** | **118** | | **Zero failures** |

---

## Project Structure

```
cloud-native/
├── docker-compose.yml              # Full system orchestration
├── eureka-server/                   # Service Discovery
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/
│       ├── java/.../EurekaServerApplication.java
│       └── resources/application.yml
├── config-server/                   # Centralized Configuration
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/
│       ├── java/.../ConfigServerApplication.java
│       └── resources/
│           ├── application.yml
│           └── configurations/      # Per-service configs
│               ├── api-gateway.yml
│               ├── catalog-service.yml
│               └── library-api.yml
├── api-gateway/                     # API Gateway + JWT
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/java/.../gateway/
│       ├── GatewayApplication.java
│       ├── config/JwtUtil.java
│       ├── filter/JwtAuthenticationFilter.java
│       └── controller/AuthController.java
├── library-api/                     # Core Library Service
│   ├── pom.xml
│   ├── Dockerfile
│   ├── Jenkinsfile
│   └── src/
│       ├── main/java/.../api/
│       │   ├── controller/          # REST endpoints
│       │   ├── service/             # Business logic
│       │   ├── repository/          # Data access
│       │   ├── entity/              # JPA entities
│       │   ├── dto/                 # Transfer objects
│       │   ├── mapper/              # Entity-DTO mappers
│       │   └── exception/           # Error handling
│       └── test/java/.../api/
│           ├── unit/                # 58 Mockito tests
│           └── integration/         # 60 MockMvc tests
└── catalog-service/                 # Catalog + Recommendations
    ├── pom.xml
    ├── Dockerfile
    └── src/main/java/.../catalog/
        ├── controller/              # REST endpoints
        ├── service/                 # Business logic
        ├── repository/              # Data access
        ├── entity/                  # JPA entities
        ├── dto/                     # Transfer objects
        └── client/                  # Feign client + fallback
```

---

## Configuration Management

The Config Server serves per-service configurations from the `configurations/` directory. Each service fetches its config on startup via the `spring.config.import=configserver:` property.

Environment-specific settings can be added using Spring profiles:
- `library-api-dev.yml` for development
- `library-api-prod.yml` for production

---

## Related Repository

- **Library API (standalone):** [github.com/ahmedwahba47/library-api](https://github.com/ahmedwahba47/library-api) — The original REST API before cloud-native enhancement
