While broadcasting to all network machines is possible, it's not recommended as it can be insecure and potentially violate network policies. Instead, here are safer alternatives:

1. Use a well-known port (like 80 or 443) and configure your router to forward traffic to your server's IP address.

2. Use a dedicated network service like NGINX or Apache to act as a reverse proxy.

3. Use a cloud-based service like Heroku or AWS that handles network configuration for you.

4. Set up a local DNS service to map a hostname to your server's IP address.

5. Use a VPN or private network to connect your clients directly to your server.

These approaches are more secure and scalable than broadcasting to all network machines.