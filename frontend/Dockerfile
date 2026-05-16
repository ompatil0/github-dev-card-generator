FROM nginx:alpine

# Copy index.html as a template
COPY index.html /usr/share/nginx/html/index.html.template

# Create an entrypoint script to substitute BACKEND_URL at runtime
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'envsubst "\$BACKEND_URL" < /usr/share/nginx/html/index.html.template > /usr/share/nginx/html/index.html' >> /entrypoint.sh && \
    echo 'exec nginx -g "daemon off;"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

EXPOSE 80

# Default backend URL (can be overridden in docker-compose)
ENV BACKEND_URL=http://localhost:8080

ENTRYPOINT ["/entrypoint.sh"]
