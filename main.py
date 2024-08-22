import os
import sys
import json
import subprocess

from pwd import getpwnam
from datetime import datetime



def get_home_fs(user: str) -> str:
    return getpwnam(user).pw_dir


class LustreQuota:
    def __init__(self, account: str, filesystem: str):
        self.account = account
        self.account_id = str(getpwnam(self.account).pw_uid)
        self.filesystem = filesystem if filesystem.startswith('/') else f'/{filesystem}'
        self.block_usage = None
        self.block_soft = None
        self.block_hard = None
        self.file_usage = None
        self.file_soft = None
        self.file_hard = None

    def get(self):
        p = subprocess.Popen(['lfs', 'quota', '-p', self.account_id, self.filesystem],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        for line in output.decode('ASCII').splitlines():
            if self.filesystem in line:
                quota = [x.replace('*','') for x in line.split()]
                self.block_usage = int(quota[1])
                self.block_soft = int(quota[2])
                self.block_hard = int(quota[3])
                self.file_usage = int(quota[5])
                self.file_soft = int(quota[6])
                self.file_hard = int(quota[7])
        return self

    def to_dict(self):
        return {
            "user": self.account,
            "path": self.filesystem + '/' + self.account,
            "block_usage": self.block_usage,
            "block_soft": self.block_soft,
            "block_hard": self.block_hard,
            "file_usage": self.file_usage,
            "file_soft": self.file_soft,
            "file_hard": self.file_hard
        }
    
    def to_ood_json(self):
        return {
            "user": self.account,
            "path": self.filesystem + '/' + self.account,
            "total_block_usage": self.block_usage,
            "block_limit": self.block_soft,
            "total_file_usage": self.file_usage,
            "file_limit": self.file_soft
        }


class NFSQuota:
    def __init__(self, account: str, filesystem: str):
        self.account = account
        self.filesystem = filesystem
        self.total_block_usage = None
        self.block_limit = None
        self.total_file_usage = None
        self.file_limit = None

    def get(self):
        quota = os.statvfs(self.filesystem)
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

class Quotas:
    def __init__(self, user: str):
        self.user = user
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


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else None
    user_home = get_home_fs(user)
    quotas = Quotas(user)
    quotas.add_nfs_quota(NFSQuota(user, user_home).get())
    quotas.add_lustre_quota(LustreQuota(user, '/projects').get())
    quotas.add_lustre_quota(LustreQuota(user, '/scratch').get())
    content = quotas.to_ood_json()
    user_home = get_home_fs(user)
    with open(f'{user_home}/ondemand/.quota.json', 'w') as outfile:
        json.dump(content, outfile, indent=4)
    print(json.dumps(content, indent=4))


if __name__ == "__main__":
    main()
