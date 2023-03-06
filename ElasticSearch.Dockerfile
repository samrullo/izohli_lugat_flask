FROM docker.elastic.co/elasticsearch/elasticsearch:7.15.1

# Install any additional plugins or dependencies
# RUN elasticsearch-plugin install analysis-icu

# Copy any additional configuration files
COPY elasticsearch.yml /usr/share/elasticsearch/config/
