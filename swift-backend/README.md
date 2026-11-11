# Fragile-Baby Server-Side Swift backend

Swift 6 / Vapor service boundary for Fragile-Baby. This service is an orchestration and qualification API only; it does not claim to control physical E2K/Elbrus hardware without explicit, authenticated host-side adapters and validated device contracts.

Run: `cd swift-backend && swift test && swift run fragilebaby-server`.

Configuration: `HOST`, `PORT`, `SERVICE_NAME`, `SERVICE_VERSION`. Secrets are external deployment inputs, never committed values.

Endpoints: `GET /health`, `GET /ready`, `GET /v1/health`. Readiness currently checks process state only. Trace IDs are propagated through `X-Trace-ID`.

Core includes immutable Sendable request context, validated Codable configuration, API error DTO, async repository contract and trace/security-header middleware. Use parameterized SQL, bounded connection pools, explicit service-level transaction boundaries and nonblocking I/O.

Production gates: database/cache providers, JWT/RBAC, TLS, OpenTelemetry, Prometheus, migrations, rate limiting, OpenAPI, load tests and Kubernetes. No production readiness is implied until these are configured and tested.
