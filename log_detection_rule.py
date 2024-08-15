from datadog_api_client.v1.api import monitors_api
from datadog_api_client.v1.models import *

with ApiClient(configuration) as api_client:
    api_instance = monitors_api.MonitorsApi(api_client)
    
    query = """
    logs("source:your_log_source AND @role:(-\"admin\" -\"file_owner\" -\"backup_service\")").index("main").rollup("count").by("role,file_path").last("5m") > 0
    """
    
    options = MonitorOptions(
        notify_no_data=False,
        thresholds={"critical": 1},
    )
    
    message = "Unauthorized File Access Detected: Role {{role.name}} accessed {{file_path.name}}."
    
    monitor = Monitor(
        name="Unauthorized Roles Detection",
        type="log alert",
        query=query,
        message=message,
        tags=["security", "unauthorized_access"],
        priority=1,
        options=options
    )
    
    api_instance.create_monitor(monitor)
