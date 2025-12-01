from typing import Dict, List, Tuple
from io import StringIO
import csv

class CSVFormatter:

    # def format_summary(self, summary: str, indent: Optional[int] = None) -> str:
    #     """Retorna un CSV valido"""
    #     out = StringIO()
    #     writer = csv.writer(out)
    #     writer.writerow(["IP", "Count"])
    #     writer.writerows()
        # return json.dumps(summary, indent=indent)

    def format_top_ips(self, top_ips: List[Tuple[str, int]]) -> str:
        """Retorna un CSV con las IP - count top"""
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(["IP", "Count"])
        writer.writerows(top_ips)
        return out.getvalue()

    def format_top_paths(self, top_paths: List[Tuple[str, int]]) -> str:
        """Retorna un CSV con los path - count top"""
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(["Paths", "Count"])
        writer.writerows(top_paths)
        return out.getvalue()

    def format_status_counts(self, status_counts: Dict[int, int]) -> str:
        """Retorna un CSV con los status - count top"""
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(["Status", "Count"])
        writer.writerows(list(status_counts.items()))
        return out.getvalue()
