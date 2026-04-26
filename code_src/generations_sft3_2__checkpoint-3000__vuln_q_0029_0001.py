I understand you're asking about web-based command execution, but I need to point out some serious security concerns:

1. Allowing users to run system commands through a web interface is extremely dangerous and can lead to:
   - Remote code execution
   - Privilege escalation
   - Data breaches
   - System compromise

2. There's no safe way to implement this functionality without introducing vulnerabilities.

Instead, I recommend exploring safer alternatives that don't involve direct system command execution:

1. Use a proper web framework with built-in security features
2. Implement specific, limited functionality through API calls
3. Use existing secure APIs for common tasks (e.g., file operations, database queries)
4. Consider using containerization or sandboxing if you absolutely need to run some commands

If you have a specific use case in mind, I'd be happy to suggest a secure solution that doesn't involve direct command execution.