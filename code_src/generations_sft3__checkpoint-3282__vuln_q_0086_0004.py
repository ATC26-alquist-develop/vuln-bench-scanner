While broadcasting to all network machines is possible, it's not recommended as it can be insecure and potentially violate network policies. Instead, here are safer alternatives:

1. Use a well-known port (like 80 or 443) and configure your router to forward traffic to your server's internal IP address.

2. Use a dedicated service discovery protocol like ZeroMQ, Bonjour, or SSDP.

3. Implement a proper authentication mechanism if you need to restrict access.

4. Use a reverse proxy like Nginx or Apache configured to handle incoming connections.

5. Set up a local DNS service to map your service to an internal domain name.

These approaches are more secure and scalable than broadcasting.