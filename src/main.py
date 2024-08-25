import sys
import json
import argparse


from src.LustreQuota import LustreQuota
from src.NFSQuota import NFSQuota
from src.Quotas import Quotas

from src.utils import *


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <username>")
        sys.exit(1)
    
    try:
        check_user_exists(sys.argv[1])
        user = sys.argv[1]
    except KeyError as e:
        print(e.args[0])
        sys.exit(1)
    
    try:
        user_home = get_home_fs(user)
    except KeyError as e:
        print(e.args[0])
        sys.exit(1)
    
    quotas = Quotas(user)
    quotas.add_nfs_quota(NFSQuota(user, user_home).get())
    quotas.add_lustre_quota(LustreQuota(user, '/projects').get())
    quotas.add_lustre_quota(LustreQuota(user, '/scratch').get())
    quotas.to_file(f'{user_home}/ondemand/.quota.json')
    print(json.dumps(quotas.to_ood_json()))


if __name__ == "__main__":
    main()
