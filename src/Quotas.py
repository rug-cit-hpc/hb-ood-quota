import json

from datetime import datetime

from src.LustreQuota import LustreQuota
from src.NFSQuota import NFSQuota


class Quotas:
    def __init__(self, user: str):
        self.user = user if user else None
        self.quotas = []

    def add_lustre_quota(self, quota: LustreQuota):
        self.quotas.append(quota)

    def add_nfs_quota(self, quota: NFSQuota):
        self.quotas.append(quota)

    def to_ood_json(self):
        return {
            "version": 1,
            "timestamp": int(datetime.timestamp(datetime.now())),
            "quotas": [quota.to_ood_json() for quota in self.quotas]
        }

    def to_file(self, file_path: str):
        try:
            with open(file_path, 'w') as outfile:
                json.dump(self.to_ood_json(), outfile, indent=4)
        except PermissionError as e:
            raise PermissionError(f"Error saving quotas to file {file_path}, no write permissions")
    