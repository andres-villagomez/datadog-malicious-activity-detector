from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api import logs_pipelines_api
from datadog_api_client.v1.models import *

# Configure API key authorization: apiKeyAuth
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = logs_pipelines_api.LogsPipelinesApi(api_client)
    
    grok_parser = LogsGrokParser(
        source="message",
        name="Extract role and file_path",
        samples=["user accessed path=/etc/passwd with role=guest"],
        grok={
            "support_rules": [],
            "match_rules": "%{DATA:file_path} path=%{GREEDYDATA:file_path} %{DATA:role} role=%{GREEDYDATA:role}"
        }
    )
    
    processor = LogsProcessor(
        type="grok_parser",
        grok_parser=grok_parser
    )
    
    pipeline = LogsPipeline(
        name="Parse role and file_path",
        is_enabled=True,
        filter=LogsFilter(query="source:your_log_source"),
        processors=[processor]
    )
    
    api_instance.create_logs_pipeline(pipeline)
