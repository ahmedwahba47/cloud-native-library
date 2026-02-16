"""
Cloud-Native System Report Content
Microservices Architecture Assignment
Student: Ahmed Wahba (A00336722)
"""

REPORT_CONTENT = {
    "title": "Cloud-Native Distributed System",
    "subtitle": "Microservices Architecture Assignment",
    "student": "Ahmed Wahba",
    "student_id": "A00336722",
    "module": "Microservices Architecture",

    "sections": [
        {
            "title": "1. Introduction and System Context",
            "content": """
This report presents the design and implementation of a cloud-native distributed system built using Spring Cloud and related technologies. The system extends a Library Management REST API into a multi-service architecture that demonstrates key cloud-native patterns: service discovery, centralised configuration, API gateway routing, inter-service communication, resilience, distributed tracing, and security.

**System Purpose:**
The system manages a library's book catalogue, loan operations, reading lists, and book recommendations. It is decomposed into two business services: a Library API (Service B) that owns book and loan data, and a Catalog Service (Service A) that owns reading lists and recommendations. Service A depends on Service B to verify book existence when adding items to reading lists or creating recommendations.

**Cloud-Native Principles Applied:**
The Twelve-Factor App methodology (Wiggins, 2017) guides the architecture. Each service is independently deployable, stateless, and configured via environment variables or a centralised configuration server. The system embraces failure as a normal operating condition, implementing circuit breakers and fallback responses to maintain partial availability when individual services fail.

**Why Cloud-Native:**
A monolithic architecture would couple all features into a single deployment unit, making independent scaling and fault isolation impossible. By decomposing into microservices, each service can be scaled, deployed, and updated independently. Newman (2021) identifies this as the key benefit of microservices: enabling organisational and technical autonomy while maintaining system-level cohesion through well-defined interfaces.

**Technology Choices:**
- **Spring Cloud** provides a cohesive ecosystem of cloud-native patterns that integrate seamlessly with Spring Boot
- **Netflix Eureka** for service discovery: mature, battle-tested in production at scale
- **Spring Cloud Gateway** for API routing: reactive, non-blocking, integrates with Eureka for dynamic route resolution
- **Resilience4j** for fault tolerance: lightweight, designed for Java 17+, replaces the deprecated Netflix Hystrix
- **Micrometer Tracing with Zipkin** for observability: standardised tracing API with automatic context propagation
"""
        },
        {
            "title": "2. Architecture Overview",
            "content": """
The system architecture diagram above illustrates how the six components communicate over a shared Docker network.

**Component Responsibilities:**

1. **Eureka Server (Port 8761)** - Service Discovery
   - Maintains a registry of all running service instances
   - Services register at startup and send periodic heartbeats
   - Clients query Eureka to resolve service names to network locations (Netflix, 2024)
   - Eliminates hardcoded URLs, enabling dynamic scaling

2. **Config Server (Port 8888)** - Centralised Configuration
   - Serves configuration properties to all services via HTTP
   - Uses native file-based storage with environment-specific profiles
   - Registered with Eureka for discoverability
   - Enables configuration changes without redeployment

3. **API Gateway (Port 8080)** - Entry Point
   - Single entry point for all client requests
   - Routes requests to services using Eureka service discovery (lb:// URIs) (Spring, 2024b)
   - Enforces JWT authentication on protected endpoints
   - Provides a token generation endpoint for authentication

4. **Library API - Service B (Port 8081)** - Book and Loan Management
   - Owns Book and Loan entities with full CRUD operations
   - Existing REST API from Assignment 1, enhanced with Eureka registration and distributed tracing
   - H2 in-memory database for development

5. **Catalog Service - Service A (Port 8082)** - Reading Lists and Recommendations
   - Owns ReadingList and Recommendation entities
   - Calls Library API via Feign client to verify book existence
   - Implements circuit breaker and retry patterns for inter-service calls
   - Provides fallback responses when Service B is unavailable

6. **Zipkin (Port 9411)** - Distributed Tracing
   - Collects trace data from all services via Micrometer Tracing
   - Visualises request flow across service boundaries
   - Enables latency analysis and bottleneck identification

**Communication Patterns:**
- **Synchronous REST:** Service A calls Service B via Feign (declarative HTTP client)
- **Service Discovery:** All inter-service communication resolves via Eureka, not hardcoded URLs
- **Load Balancing:** Spring Cloud LoadBalancer provides client-side load balancing across instances
"""
        },
        {
            "title": "3. Service Discovery and Interaction",
            "content": """
**Service Discovery Pattern:**
Service discovery solves the fundamental problem of locating services in a dynamic environment where instances can start, stop, and move across hosts. Without service discovery, services would require hardcoded URLs, making the system fragile and preventing dynamic scaling (Richardson, 2018).

**Eureka Implementation:**
The system uses Netflix Eureka in a client-server model:

**Server Configuration:**
```
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
  server:
    enable-self-preservation: false
```

The Eureka server does not register with itself. Self-preservation is disabled for development to ensure deregistered services are removed promptly.

**Client Registration:**
Each service includes `spring-cloud-starter-netflix-eureka-client` and configures:
```
eureka:
  client:
    service-url:
      defaultZone: http://eureka-server:8761/eureka/
  instance:
    prefer-ip-address: true
```

Services register using their `spring.application.name` as the service identifier. The `prefer-ip-address` setting ensures containers are reachable across the Docker network.

**Service-to-Service Communication:**
The Catalog Service communicates with the Library API using Spring Cloud OpenFeign:

```
@FeignClient(name = "library-api",
             fallback = LibraryApiClientFallback.class)
public interface LibraryApiClient {
    @GetMapping("/api/books/{id}")
    BookDTO getBookById(@PathVariable("id") Long id);
}
```

The `name` attribute matches the Library API's registered name in Eureka. Spring Cloud automatically resolves this to the actual host and port via service discovery. The `fallback` attribute specifies a class that provides default responses when the service is unavailable.

**Why Feign Over RestTemplate/WebClient:**
Feign provides a declarative HTTP client that reduces boilerplate. The interface-based approach makes service contracts explicit and testable. Combined with Eureka integration, it automatically handles service resolution and client-side load balancing (Spring, 2024a).
"""
        },
        {
            "title": "4. Configuration Management",
            "content": """
**The Configuration Problem:**
In a distributed system, each service requires configuration for database connections, service URLs, feature flags, and environment-specific settings. Embedding configuration in application code or per-service files creates maintenance overhead and requires redeployment for configuration changes (Newman, 2021).

**Spring Cloud Config Server:**
The Config Server externalises configuration into a central location. It uses the "native" profile to serve configuration from classpath files:

```
spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/configurations
```

Configuration files are named by service: `library-api.yml`, `catalog-service.yml`, `api-gateway.yml`. The Config Server is itself registered with Eureka, allowing services to discover it dynamically.

**Configuration Structure:**
Each service's configuration is stored in a separate file under `/configurations/`:

- **library-api.yml** - Server port, datasource, JPA settings, tracing configuration
- **catalog-service.yml** - Server port, datasource, Resilience4j circuit breaker and retry settings
- **api-gateway.yml** - Gateway routes, management endpoints

**Environment-Specific Configuration:**
Spring profiles enable environment-specific overrides. For production, files like `library-api-prod.yml` can override development defaults with PostgreSQL connection details and production-appropriate settings.

**Configuration Priority:**
Spring Boot's property resolution order ensures flexibility:
1. Environment variables (highest priority - used in Docker)
2. Config Server properties
3. Local application.yml (lowest priority)

This allows Docker environment variables to override Config Server defaults, which is essential for containerised deployments where database hosts and service URLs differ from development.

**Why Centralised Configuration:**
- **Single source of truth:** All service configurations are managed in one location
- **No redeployment:** Configuration changes can be applied without rebuilding service images
- **Environment parity:** The same service image runs in dev and prod with different configurations
- **Auditability:** Configuration changes are version-controlled alongside infrastructure code
"""
        },
        {
            "title": "5. Resilience and Fault Handling",
            "content": """
**The Resilience Problem:**
In a distributed system, any service can fail at any time due to network issues, resource exhaustion, or bugs. Without resilience patterns, a single service failure can cascade through the system, causing total outage. This is known as cascading failure (Nygard, 2018).

**Resilience4j Implementation:**
The Catalog Service implements two Resilience4j patterns for calls to the Library API:

**1. Circuit Breaker:**
```
resilience4j:
  circuitbreaker:
    instances:
      libraryApi:
        sliding-window-size: 10
        minimum-number-of-calls: 5
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
```

The circuit breaker monitors the last 10 calls. If 50% or more fail (after a minimum of 5 calls), the circuit opens, blocking further requests for 10 seconds. After this period, the circuit enters half-open state, allowing 3 test calls to determine if the service has recovered (Resilience4j, 2024).

**Circuit Breaker States:**
- **Closed (normal):** Requests flow through; failures are counted
- **Open (tripped):** Requests are immediately rejected; fallback is invoked
- **Half-Open (testing):** Limited requests are allowed to test recovery

**2. Retry with Exponential Backoff:**
```
resilience4j:
  retry:
    instances:
      libraryApi:
        max-attempts: 3
        wait-duration: 1s
        exponential-backoff-multiplier: 2
```

Before the circuit breaker opens, transient failures are retried up to 3 times with exponential backoff (1s, 2s, 4s). This handles temporary network glitches without immediately tripping the circuit breaker.

**Fallback Responses:**
When the circuit is open or retries are exhausted, fallback methods provide degraded but functional responses:

```
public ReadingListDTO addBookFallback(
        Long readingListId,
        AddBookRequest request,
        Throwable t) {
    // Add book without verification
    // Mark as [unverified]
}
```

The Feign client also has a fallback class that returns placeholder data:
```
public BookDTO getBookById(Long id) {
    return BookDTO.builder()
        .id(id).title("Unavailable")
        .author("Unavailable").build();
}
```

**Why This Approach:**
The combination of retry, circuit breaker, and fallback provides defence in depth. Retries handle transient failures (network blips). The circuit breaker prevents resource exhaustion during sustained failures. Fallbacks maintain partial system functionality, allowing users to continue working even when a dependency is down.
"""
        },
        {
            "title": "6. Observability",
            "content": """
**The Observability Challenge:**
In a distributed system, a single user request may traverse multiple services. When failures or performance issues occur, identifying the root cause requires tracing the request's path across service boundaries. Traditional logging is insufficient because logs are scattered across services with no correlation (Richardson, 2018).

**Distributed Tracing with Micrometer and Zipkin:**
The system uses Micrometer Tracing (the successor to Spring Cloud Sleuth) with Brave as the tracing implementation and Zipkin as the trace collector and visualiser.

**Trace Propagation:**
Each incoming request is assigned a trace ID that propagates across all service calls:

1. Client sends request to API Gateway
2. Gateway assigns trace ID, forwards to Library API or Catalog Service
3. Catalog Service's Feign client propagates the trace ID to Library API
4. All services report spans to Zipkin

**Configuration:**
```
management:
  tracing:
    sampling:
      probability: 1.0
  zipkin:
    tracing:
      endpoint: http://zipkin:9411/api/v2/spans
```

A sampling probability of 1.0 traces every request (appropriate for development; production would use a lower value).

**What Zipkin Reveals:**
- **Request flow:** Visual timeline showing which services were called and in what order
- **Latency breakdown:** Time spent in each service, identifying bottlenecks
- **Error location:** Which service in the chain caused a failure
- **Dependency mapping:** Auto-generated service dependency graph

**Health Endpoints:**
Each service exposes Spring Boot Actuator endpoints for operational monitoring:
- `/actuator/health` - Service health status (used by Docker health checks)
- `/actuator/info` - Service metadata
- `/actuator/circuitbreakers` - Circuit breaker state (Catalog Service)

**Why Micrometer Tracing:**
Micrometer Tracing is the official replacement for Spring Cloud Sleuth in Spring Boot 3.x. It provides a vendor-neutral tracing API, allowing the system to switch from Zipkin to Jaeger or other backends without code changes. The auto-configuration ensures trace context is propagated through Feign clients, RestTemplates, and WebClients automatically (Spring, 2024c).
"""
        },
        {
            "title": "7. Security Considerations",
            "content": """
**Security in Microservices:**
A distributed system has a larger attack surface than a monolith. Each service is a potential entry point, and inter-service communication must be secured to prevent unauthorised access. The API Gateway pattern centralises authentication at the system boundary, reducing the security burden on individual services (Richardson, 2018).

**JWT Authentication at the Gateway:**
The API Gateway enforces JWT (JSON Web Token) authentication using a global filter:

```
public class JwtAuthenticationFilter
    implements GlobalFilter, Ordered {

    public Mono<Void> filter(
            ServerWebExchange exchange,
            GatewayFilterChain chain) {
        // Extract and validate JWT from
        // Authorization header
    }
}
```

**Authentication Flow:**
1. Client requests a token from `POST /api/auth/token` with credentials
2. Gateway generates a signed JWT with subject claim and expiration
3. Client includes the JWT in subsequent requests as `Authorization: Bearer <token>`
4. Gateway validates the token signature and expiration before routing
5. Invalid or expired tokens receive HTTP 401 Unauthorized

**Token Structure:**
JWTs are signed using HMAC-SHA256 with a configurable secret key. The token contains:
- **Subject:** Username
- **Issued At:** Token creation timestamp
- **Expiration:** Token validity period (default: 1 hour)

**Open Endpoints:**
The token generation endpoint (`/api/auth/token`) and actuator health endpoints are excluded from authentication to allow initial token acquisition and infrastructure monitoring.

**Trust Boundaries:**
- **External boundary (Gateway):** All external requests must include a valid JWT
- **Internal boundary (Service-to-Service):** Services communicate within the Docker network without JWT verification, as the network boundary provides isolation
- **Data boundary:** Each service owns its database; cross-service data access is only via REST APIs

**Security Limitations and Future Improvements:**
- Current implementation uses a shared secret; production should use RSA key pairs
- No role-based access control (RBAC); all authenticated users have equal access
- Inter-service communication trusts the network boundary; mutual TLS (mTLS) would add defence in depth
- Token refresh is not implemented; clients must request new tokens after expiration

**Why JWT Over Session-Based Authentication:**
JWTs are stateless, meaning the gateway does not need to maintain session storage. This aligns with the Twelve-Factor App principle of stateless processes and enables horizontal scaling of the gateway without session affinity (Wiggins, 2017).
"""
        },
        {
            "title": "8. Evaluation and Reflection",
            "content": """
**What Works Well:**

1. **Service Independence:** Each service is independently deployable with its own database, codebase, and lifecycle. The Catalog Service can be updated without affecting the Library API.

2. **Resilience:** The circuit breaker pattern ensures the Catalog Service remains functional when the Library API is unavailable. Fallback responses provide degraded but usable functionality, preventing cascading failures.

3. **Dynamic Discovery:** Adding a new service instance requires no configuration changes to other services. Eureka handles registration and discovery automatically, enabling horizontal scaling.

4. **Centralised Observability:** Zipkin provides a unified view of request flow across all services, making debugging distributed issues practical.

5. **Gateway Security:** JWT authentication at the gateway provides a single enforcement point, simplifying the security model for individual services.

**Conscious Trade-offs:**

1. **H2 vs PostgreSQL:** Development uses H2 in-memory databases for speed. This means database-specific features (stored procedures, advanced indexes) are not tested. Mitigation: the system is designed for database portability via JPA abstraction.

2. **Synchronous Communication:** Service A calls Service B synchronously via REST. Under high load, this creates coupling where Service A's response time depends on Service B's latency. An asynchronous approach (message queues) would decouple response times but add complexity beyond the assignment scope.

3. **Single Eureka Instance:** Production systems run multiple Eureka instances for high availability. Our single instance is a single point of failure. Mitigation: services cache the registry locally, allowing continued operation if Eureka temporarily fails.

**Limitations:**

- No automated testing of the distributed system (end-to-end tests across services)
- No container orchestration (Kubernetes would provide self-healing, scaling, and rolling updates)
- No centralised logging aggregation (ELK stack or similar)
- No rate limiting at the gateway
- No service mesh for advanced traffic management

**Suggested Improvements:**

1. **Kubernetes Deployment** - Replace Docker Compose with Kubernetes manifests for production-grade orchestration with auto-scaling, self-healing, and rolling updates
2. **Asynchronous Events** - Introduce Apache Kafka or RabbitMQ for event-driven communication between services, reducing temporal coupling
3. **Centralised Logging** - Add ELK stack (Elasticsearch, Logstash, Kibana) for aggregated log search across all services
4. **Mutual TLS** - Implement mTLS between services using a service mesh (Istio) for zero-trust networking
"""
        },
        {
            "title": "9. GitHub Repository",
            "content": """
**Cloud-Native Repository:** https://github.com/ahmedwahba47/cloud-native-library

**Repository Structure:**
- `eureka-server/` - Service Discovery (Netflix Eureka)
- `config-server/` - Centralised Configuration (Spring Cloud Config)
- `api-gateway/` - API Gateway with JWT authentication (Spring Cloud Gateway)
- `catalog-service/` - Service A (Reading Lists, Recommendations, Feign client, Resilience4j)
- `library-api/` - Service B (Enhanced with Eureka, Config, Tracing)
- `docker-compose.yml` - Full system orchestration

**Library API (standalone):** https://github.com/ahmedwahba47/library-api
"""
        },
        {
            "title": "10. References",
            "content": """
Newman, S. (2021) Building Microservices: Designing Fine-Grained Systems. 2nd edn. Sebastopol: O'Reilly Media.

Nygard, M. (2018) Release It! Design and Deploy Production-Ready Software. 2nd edn. Raleigh: Pragmatic Bookshelf.

Richardson, C. (2018) Microservices Patterns: With Examples in Java. Shelter Island: Manning Publications.

Spring (2024a) Spring Cloud Documentation. Available at: https://spring.io/projects/spring-cloud (Accessed: 10 February 2026).

Spring (2024b) Spring Cloud Gateway Documentation. Available at: https://docs.spring.io/spring-cloud-gateway/reference/ (Accessed: 10 February 2026).

Spring (2024c) Micrometer Tracing Documentation. Available at: https://docs.micrometer.io/tracing/reference/ (Accessed: 10 February 2026).

Netflix (2024) Eureka Wiki. Available at: https://github.com/Netflix/eureka/wiki (Accessed: 10 February 2026).

Resilience4j (2024) Resilience4j Documentation. Available at: https://resilience4j.readme.io/docs (Accessed: 10 February 2026).

Wiggins, A. (2017) The Twelve-Factor App. Available at: https://12factor.net/ (Accessed: 10 February 2026).
"""
        }
    ]
}
