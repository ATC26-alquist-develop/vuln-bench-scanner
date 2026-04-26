While it's possible to implement a web interface for running system commands, this poses significant security risks and should be avoided. Instead, I recommend using a more secure approach:

1. Use a proper web framework with built-in security features
2. Implement authentication and authorization
3. Use parameterized queries for any database operations
4. Implement proper input validation and sanitization
5. Use a content security policy
6. Implement rate limiting and other security measures

If you need to execute system commands, consider using a dedicated API or a secure remote execution service instead of directly exposing command execution through a web interface.