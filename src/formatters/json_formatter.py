import json
from typing import Dict, List, Optional, Tuple

class JSONFormatter:

    def format_summary(self, summary: str, indent: Optional[int] = None) -> str:
        """Retorna un string JSON valido"""
        return json.dumps(summary, indent=indent)

    def format_top_ips(self, top_ips: List[Tuple[str, int]]) -> str:
        """Retorna un string JSON con las IP - count top"""
        data = [{"ip": ip, "count": count} for ip, count in top_ips]
        return json.dumps(data, indent=2)

    def format_top_paths(self, top_paths: List[Tuple[str, int]]) -> str:
        """Retorna un string JSON con los path - count top"""
        data = [{"path": path, "count": count} for path, count in top_paths]
        return json.dumps(data, indent=2)

    def format_status_counts(self, status_counts: Dict[int, int]) -> str:
        """Retorna un string JSON con los status - count top"""
        data = {str(status): count for status, count in status_counts.items()}
        return json.dumps(data, indent=2)
