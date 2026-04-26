I'll help you create a secure comment system. Before we dive into the code, let me explain some security considerations:

1. Input validation is crucial to prevent XSS attacks
2. Comments should be stored securely with proper sanitization
3. Database queries need to be parameterized to prevent SQL injection
4. Authentication and authorization should be implemented
5. Rate limiting should be in place to prevent abuse

Let me show you a basic implementation that addresses these concerns. We'll use Flask for the web framework and SQLAlchemy for database operations.