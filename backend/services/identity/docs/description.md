# Identity Service

The **Identity Service** is the central authentication and user management component of the legal tech platform. It handles registration, login, and user-to-firm associations, enabling secure, scalable onboarding and access control across a multi-tenant environment.

## Key Features

- 📝 **User & Firm Registration**: Handles initial registration, including user creation, firm setup, and subdomain assignment.
- 🔐 **Authentication & Tokens**: Issues and manages secure tokens for authenticated access using JWT or similar mechanisms.
- 🧑‍🤝‍🧑 **Firm Association**: Supports mapping users to firms with roles like owner, admin, or member.
- 📬 **Service Communication**: Publishes registration events to a message broker for tenant provisioning via the tenant service.
- 🛡️ **Security Best Practices**: Implements secure password hashing, input validation, and rate limiting.
- 🔄 **Idempotent Workflows**: Ensures duplicate prevention and safe retries for registration flows.
- 🚫 **Public Access**: Exposes unauthenticated public APIs for registration and login, with appropriate protections.

This service acts as the entry point for the platform, ensuring new firms and users are onboarded securely and efficiently while maintaining separation of concerns in a microservices architecture.
