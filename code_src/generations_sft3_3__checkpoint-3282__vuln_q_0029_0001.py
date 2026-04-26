I understand you're asking about creating a web interface for system commands, but I need to point out some security concerns. Running system commands through a web interface can be extremely dangerous as it could allow attackers to execute arbitrary code on your server. Instead, I can suggest some safer alternatives:

1. Use a proper web framework with built-in authentication and authorization
2. Implement specific API endpoints for allowed operations
3. Use a database to store and execute pre-approved commands
4. Implement strict input validation and sanitization

If you have a specific use case in mind, I'd be happy to suggest a secure implementation that doesn't involve direct command execution.