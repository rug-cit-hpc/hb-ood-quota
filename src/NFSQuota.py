import os

class NFSQuota:
    def __init__(self, account: str, filesystem: str):
        self.account = account
        self.filesystem = filesystem
        self.total_block_usage = None
        self.block_limit = None
        self.total_file_usage = None
        self.file_limit = None

    def get(self):
        try:
            quota = os.statvfs(self.filesystem)
        except FileNotFoundError:
            return None
        self.total_block_usage = (quota.f_blocks - quota.f_bavail) * quota.f_frsize // 1024
        self.block_limit = quota.f_blocks * quota.f_frsize // 1024
        self.total_file_usage = quota.f_files - quota.f_favail
        self.file_limit = quota.f_files
        return self

    def to_ood_json(self):
        return {
            "user": self.account,
            "path": self.filesystem,
            "total_block_usage": self.total_block_usage,
            "block_limit": self.block_limit,
            "total_file_usage": self.total_file_usage,
            "file_limit": self.file_limit
        }
