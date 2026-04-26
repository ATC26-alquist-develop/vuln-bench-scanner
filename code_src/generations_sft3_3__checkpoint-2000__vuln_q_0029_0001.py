I understand you're asking about creating a web interface for system commands, but I need to point out some security concerns:

1. Allowing arbitrary system commands through a web interface is extremely dangerous and could lead to severe security vulnerabilities.

2. It could potentially be used for:
   - Remote code execution
   - Privilege escalation
   - Data exfiltration
   - System compromise

3. Even with input sanitization, it's extremely difficult to make such a system 100% secure.

Instead, I recommend exploring safer alternatives:

1. Use a proper web framework with built-in security features
2. Implement specific, controlled API endpoints for required actions
3. Use role-based access control
4. Implement proper authentication and authorization
5. Sanitize and validate all user inputs
6. Use principle of least privilege

If you have a specific use case in mind, I'd be happy to suggest a secure implementation that meets your needs without introducing vulnerabilities.