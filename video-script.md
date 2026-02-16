# Cloud-Native System Video Script
## Microservices Architecture Assignment
### Student: Ahmed Wahba (A00336722)
### Duration: 10 minutes

---

## 0:00 - 0:45 | System Context and Intent (45 seconds)

**[Screen: Architecture diagram or system overview]**

"Hello, I'm Ahmed Wahba. This video demonstrates a cloud-native distributed system built using Spring Cloud.

The system extends a Library Management API into a multi-service architecture with two business services, an API gateway, service discovery, centralised configuration, distributed tracing, and JWT security.

**[Show architecture diagram]**

The core question this system answers is: how do we decompose a monolith into independently deployable services while maintaining reliability, observability, and security?

I'll demonstrate each cloud-native pattern in action, including what happens when a service fails."

---

## 0:45 - 1:45 | Architecture Overview (60 seconds)

**[Screen: Architecture diagram with port numbers]**

"Let me walk through the architecture.

**[Point to each component]**

We have six components:

1. **Eureka Server** on port 8761 — service discovery registry where all services register
2. **Config Server** on port 8888 — centralised configuration serving properties to all services
3. **API Gateway** on port 8080 — single entry point for clients, handles JWT authentication and routes to services via Eureka
4. **Library API (Service B)** on port 8081 — owns books and loans, the existing REST API enhanced with cloud-native features
5. **Catalog Service (Service A)** on port 8082 — owns reading lists and recommendations, calls Service B via Feign to verify books
6. **Zipkin** on port 9411 — collects and visualises distributed traces

All services communicate via a shared Docker network. Service A depends on Service B — this is where resilience patterns become critical.

**[Show docker-compose.yml briefly]**

Docker Compose orchestrates the startup order: Eureka first, then Config Server, then the business services, and finally the Gateway."

---

## 1:45 - 2:45 | Gateway and Service Discovery (60 seconds)

**[Screen: Terminal showing docker-compose up]**

"Let me start the system and demonstrate service discovery.

**[Show Eureka dashboard at localhost:8761]**

Here's the Eureka dashboard. You can see all four services registered: api-gateway, library-api, catalog-service, and config-server. Each shows its status as UP with its host and port.

The key point is that no service has a hardcoded URL to another service. The API Gateway routes to `lb://library-api` — that `lb://` prefix tells Spring Cloud to resolve the hostname via Eureka and load balance across instances.

**[Show gateway routes]**

The gateway routes `/api/books/**` and `/api/loans/**` to the Library API, and `/api/reading-lists/**` and `/api/recommendations/**` to the Catalog Service.

**[Demonstrate a request through the gateway]**

```bash
# Get a JWT token first
curl -X POST http://localhost:8080/api/auth/token \
  -H 'Content-Type: application/json' \
  -d '{"username": "ahmed"}'

# Use token to access books through gateway
curl http://localhost:8080/api/books \
  -H 'Authorization: Bearer <token>'
```

The request enters the gateway on port 8080, is authenticated, routed to Service B on 8081 via Eureka, and the response flows back."

---

## 2:45 - 3:45 | Configuration Management (60 seconds)

**[Screen: Config Server files and endpoints]**

"The Config Server centralises configuration for all services.

**[Show config-server application.yml]**

It uses Spring's native profile to serve configuration from classpath files. Each service has its own configuration file.

**[Show the configuration files]**

For example, `catalog-service.yml` contains the Resilience4j circuit breaker settings, database configuration, and tracing settings. These are served to the Catalog Service at startup.

**[Hit Config Server endpoint]**

```bash
curl http://localhost:8888/catalog-service/default
```

This returns the full configuration for the catalog service. Services can be reconfigured without rebuilding their Docker images — just update the config file and restart the Config Server.

The priority order is: environment variables override Config Server values, which override local application.yml. This is why Docker Compose can set `EUREKA_CLIENT_SERVICEURL_DEFAULTZONE` to override the Eureka URL for containerised deployment."

---

## 3:45 - 5:15 | Service-to-Service Interaction (90 seconds)

**[Screen: Terminal with curl commands]**

"Now let me demonstrate the core inter-service interaction: Catalog Service calling Library API.

**[Create a reading list]**

```bash
curl -X POST http://localhost:8080/api/reading-lists \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Spring Reading", "ownerName": "Ahmed", "description": "Cloud-native books"}'
```

Reading list created successfully in the Catalog Service.

**[Add a book to the reading list]**

```bash
curl -X POST http://localhost:8080/api/reading-lists/1/books \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"bookId": 1, "notes": "Essential reading"}'
```

**[Explain the interaction]**

This request flows through four components:
1. Gateway authenticates the JWT and routes to Catalog Service
2. Catalog Service receives the request to add book ID 1
3. Catalog Service calls Library API via Feign: `GET /api/books/1`
4. Library API returns the book details, confirming it exists
5. Catalog Service saves the reading list item with verified book data

**[Show the reading list with enriched book data]**

```bash
curl http://localhost:8080/api/reading-lists/1 \
  -H 'Authorization: Bearer <token>'
```

The response includes `bookTitle` and `bookAuthor` fetched from Service B — this is data enrichment across service boundaries."

---

## 5:15 - 6:45 | Resilience and Failure Handling (90 seconds)

**[Screen: Terminal and Docker commands]**

"Now the critical demonstration: what happens when Service B fails?

**[Stop the Library API container]**

```bash
docker stop library-api
```

Service B is now down. Let's see what happens when Service A tries to call it.

**[Try adding another book to the reading list]**

```bash
curl -X POST http://localhost:8080/api/reading-lists/1/books \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"bookId": 2, "notes": "Recommended by lecturer"}'
```

**[Show the response]**

The request still succeeds! But notice the notes field says '[unverified - library service unavailable]'. This is the circuit breaker fallback in action.

**[Explain the resilience flow]**

Here's what happened:
1. Feign client tried to call Library API — connection refused
2. Retry pattern attempted 3 times with exponential backoff (1s, 2s, 4s)
3. All retries failed, triggering the circuit breaker
4. Fallback method executed: the book was added without verification
5. The user received a response — degraded but functional

**[Show circuit breaker health]**

```bash
curl http://localhost:8082/actuator/health
```

The circuit breaker shows state OPEN. After 10 seconds, it transitions to HALF_OPEN and tests if Service B has recovered.

**[Restart Service B]**

```bash
docker start library-api
```

After restart, the circuit breaker detects recovery and returns to CLOSED state. Subsequent requests are fully verified again."

---

## 6:45 - 8:00 | Observability and Tracing (75 seconds)

**[Screen: Zipkin dashboard at localhost:9411]**

"Let me show how distributed tracing provides visibility across the system.

**[Open Zipkin UI]**

Here's the Zipkin dashboard. Every request that traverses our services is captured as a trace.

**[Click on a trace for a reading list book addition]**

This trace shows a request to add a book to a reading list. You can see:

1. **API Gateway** — receives the request, time spent routing
2. **Catalog Service** — processes the business logic
3. **Library API** — called by Catalog Service to verify the book

Each bar represents a span with start time and duration. The trace ID is the same across all three services — this is automatic context propagation via Micrometer Tracing.

**[Show a failed trace]**

Here's a trace from when Service B was down. You can see the Catalog Service spans, the retry attempts, and the fallback execution. Zipkin clearly shows where the failure occurred and how long the retries took.

**[Show dependency graph]**

Zipkin auto-generates a service dependency graph from trace data. It shows api-gateway depends on catalog-service, which depends on library-api. This is invaluable for understanding system topology in complex architectures."

---

## 8:00 - 9:00 | Security and Trust Boundaries (60 seconds)

**[Screen: Terminal with JWT demonstration]**

"Security is enforced at the API Gateway using JWT authentication.

**[Show unauthenticated request]**

```bash
curl http://localhost:8080/api/books
# Returns 401 Unauthorized
```

Without a JWT token, the gateway rejects the request immediately. The request never reaches the backend services.

**[Generate a token]**

```bash
curl -X POST http://localhost:8080/api/auth/token \
  -H 'Content-Type: application/json' \
  -d '{"username": "ahmed"}'
```

The gateway generates a signed JWT with a 1-hour expiration.

**[Use the token]**

```bash
curl http://localhost:8080/api/books \
  -H 'Authorization: Bearer eyJ...'
# Returns book data successfully
```

With a valid token, the request passes through the gateway to the Library API.

**[Explain trust boundaries]**

The trust boundary is at the gateway. Internal services communicate freely within the Docker network — this is a conscious trade-off. The network boundary provides isolation. In production, mutual TLS between services would add defence in depth."

---

## 9:00 - 10:00 | Evaluation and Reflection (60 seconds)

**[Screen: Summary or architecture diagram]**

"Let me evaluate this cloud-native implementation.

**Strengths:**
- Six components demonstrating real cloud-native patterns
- Resilience works: Service A degrades gracefully when Service B fails
- Distributed tracing provides genuine observability across service boundaries
- JWT authentication secures the system boundary with stateless tokens

**Key Trade-off:**
Synchronous REST communication between services means Service A's latency depends on Service B. An event-driven architecture with message queues would decouple this, but adds complexity beyond the scope of this assignment.

**What I'd Improve:**
- Add Kubernetes for production-grade orchestration with auto-scaling
- Implement asynchronous events with Kafka for eventual consistency
- Add mutual TLS for zero-trust inter-service communication
- Implement centralised logging with ELK stack

The system successfully demonstrates that cloud-native patterns — service discovery, configuration management, resilience, observability, and security — work together to create a robust distributed architecture. Thank you for watching."

---

## Production Notes

### Screen Recordings Needed:
1. Architecture diagram overview
2. Docker Compose startup sequence
3. Eureka dashboard with all services registered
4. Gateway routing demonstration with JWT
5. Config Server endpoint response
6. Service-to-service call (reading list + book enrichment)
7. Failure scenario: stop Service B, show fallback, show circuit breaker state
8. Zipkin traces: happy path and failure path
9. JWT authentication: unauthenticated rejection, token generation, authenticated request

### Key Points to Emphasise:
- WHY for each pattern (not just how)
- Service discovery eliminates hardcoded URLs
- Circuit breaker prevents cascading failure
- Fallback provides degraded but functional service
- Trace propagation across service boundaries
- Gateway as single security enforcement point
- All components running in Docker containers

### Timing Checklist:
- [ ] Context & Intent: 45 sec
- [ ] Architecture Overview: 60 sec
- [ ] Gateway & Service Discovery: 60 sec
- [ ] Configuration Management: 60 sec
- [ ] Service-to-Service: 90 sec
- [ ] Resilience & Failure: 90 sec
- [ ] Observability & Tracing: 75 sec
- [ ] Security: 60 sec
- [ ] Evaluation: 60 sec
- **Total: 10 minutes**
