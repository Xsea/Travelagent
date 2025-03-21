# Use the ankane/pgvector image
FROM ankane/pgvector

# Enable pgvector extension
RUN apt-get update && apt-get install -y postgresql-13-pgvector

# Set environment variables
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=pass
ENV POSTGRES_DB=vectorDB

# Copy initialization script
COPY ./initdb/init-vector.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432

# Start PostgreSQL
CMD ["postgres"]