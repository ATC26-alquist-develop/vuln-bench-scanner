While broadcasting to all network machines is possible, it's not recommended as it can be insecure and potentially violate network policies. Instead, here are safer alternatives:

1. Use a well-known port (like 80 or 443) and configure your router to forward traffic to your server's internal IP.

2. Use a reverse proxy like Nginx or Apache to handle external connections.

3. Implement proper authentication and encryption (SSL/TLS) for your server.

4. Use a dedicated service discovery protocol like Zeroconf (Bonjour) if you need to discover services on the local network.

5. Configure your firewall to allow connections to your server's external IP on the appropriate port.

Remember to always use encryption (SSL/TLS) when exposing services to the network.