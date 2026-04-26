While broadcasting to all network machines is possible, it's not recommended as it can be insecure and potentially violate network policies. Instead, here are safer alternatives:

1. Use a dedicated network service like:
- Nginx
- Apache
- Lighttpd
- Reverse proxy (like nginx or haproxy)

2. Configure your firewall to allow incoming connections on the required ports.

3. Use a proper network service discovery mechanism like:
- Bonjour (Zeroconf)
- SSDP
- UPnP

4. Implement proper authentication and encryption (SSL/TLS) for your service.

5. Use a reverse proxy setup with proper security configurations.

These approaches are more secure and scalable than broadcasting.