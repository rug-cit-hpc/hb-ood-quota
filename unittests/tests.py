import unittest
import json

from src.LustreQuota import LustreQuota
from src.Quotas import Quotas
from src.NFSQuota import NFSQuota


class TestOODQuotas(unittest.TestCase):
    def test_add_lustre_quota(self):
        user = 'p233780'
        quotas = Quotas(user)
        lustre_quota = LustreQuota(user, '/projects')
        quotas.add_lustre_quota(lustre_quota)
        self.assertEqual(len(quotas.quotas), 1)
        self.assertEqual(quotas.quotas[0], lustre_quota)
    
    def test_add_nfs_quota(self):
        user = 'p233780'
        quotas = Quotas(user)
        nfs_quota = NFSQuota(user, f'/home1/{user}').get()
        quotas.add_nfs_quota(nfs_quota)
        self.assertEqual(len(quotas.quotas), 1)
        self.assertEqual(quotas.quotas[0], nfs_quota)

    def test_to_ood_json(self):
        user = 'p233780'
        quotas = Quotas(user)
        lustre_quota = LustreQuota(user, '/projects').get()
        nfs_quota = NFSQuota(user, f'/home1/{user}').get()
        quotas.add_lustre_quota(lustre_quota)
        quotas.add_nfs_quota(nfs_quota)
        ood_json = quotas.to_ood_json()
        self.assertIsNotNone(ood_json)
        self.assertEqual(ood_json['version'], 1)
        self.assertIsNotNone(ood_json['timestamp'])
        self.assertEqual(len(ood_json['quotas']), 2)
        self.assertEqual(ood_json['quotas'][0], lustre_quota.to_ood_json())
        self.assertEqual(ood_json['quotas'][1], nfs_quota.to_ood_json())

    def test_to_file(self):
        user = 'p233780'
        quotas = Quotas(user)
        lustre_quota = LustreQuota(user, '/projects').get()
        nfs_quota = NFSQuota(user, f'/home1/{user}').get()
        quotas.add_lustre_quota(lustre_quota)
        quotas.add_nfs_quota(nfs_quota)
        file_path = f'/tmp/{user}.json'
        quotas.to_file(file_path)
        with open(file_path, 'r') as file:
            ood_json = json.load(file)
            self.assertIsNotNone(ood_json)
            self.assertEqual(ood_json['version'], 1)
            self.assertIsNotNone(ood_json['timestamp'])
            self.assertEqual(len(ood_json['quotas']), 2)
            self.assertEqual(ood_json['quotas'][0], lustre_quota.to_ood_json())
            self.assertEqual(ood_json['quotas'][1], nfs_quota.to_ood_json())


class TestLustreQuota(unittest.TestCase):
    def test_get_lustre_quota(self):
        user = 'p233780'
        lustre_quota = LustreQuota(user, '/projects').get()
        self.assertIsNotNone(lustre_quota)
        self.assertEqual(lustre_quota.account, user)
        self.assertEqual(lustre_quota.filesystem, '/projects')
        self.assertIsNotNone(lustre_quota.block_usage)
        self.assertIsNotNone(lustre_quota.block_soft)
        self.assertIsNotNone(lustre_quota.block_hard)
        self.assertIsNotNone(lustre_quota.file_usage)
        self.assertIsNotNone(lustre_quota.file_soft)
        self.assertIsNotNone(lustre_quota.file_hard)
    
    def test_to_dict(self):
        user = 'p233780'
        lustre_quota = LustreQuota(user, '/projects').get()
        self.assertIsNotNone(lustre_quota)
        quota_dict = lustre_quota.to_dict()
        self.assertIsNotNone(quota_dict)
        self.assertEqual(quota_dict['user'], user)
        self.assertEqual(quota_dict['path'], '/projects/p233780')
        self.assertIsNotNone(quota_dict['block_usage'])
        self.assertIsNotNone(quota_dict['block_soft'])
        self.assertIsNotNone(quota_dict['block_hard'])
        self.assertIsNotNone(quota_dict['file_usage'])
        self.assertIsNotNone(quota_dict['file_soft'])
        self.assertIsNotNone(quota_dict['file_hard'])
    
    def test_to_ood_json(self):
        user = 'p233780'
        lustre_quota = LustreQuota(user, '/projects').get()
        self.assertIsNotNone(lustre_quota)
        quota_json = lustre_quota.to_ood_json()
        self.assertIsNotNone(quota_json)
        self.assertEqual(quota_json['user'], user)
        self.assertEqual(quota_json['path'], '/projects/p233780')
        self.assertIsNotNone(quota_json['total_block_usage'])
        self.assertIsNotNone(quota_json['block_limit'])
        self.assertIsNotNone(quota_json['total_file_usage'])
        self.assertIsNotNone(quota_json['file_limit'])


class TestNFSQuota(unittest.TestCase):
    def test_get_nfs_quota(self):
        user = 'p233780'
        nfs_quota = NFSQuota(user, f'/home1/{user}').get()
        self.assertIsNotNone(nfs_quota)
        self.assertEqual(nfs_quota.account, user)
        self.assertEqual(nfs_quota.filesystem, f'/home1/{user}')
        self.assertIsNotNone(nfs_quota.total_block_usage)
        self.assertIsNotNone(nfs_quota.block_limit)
        self.assertIsNotNone(nfs_quota.total_file_usage)
        self.assertIsNotNone(nfs_quota.file_limit)
    
    def test_to_ood_json(self):
        user = 'p233780'
        nfs_quota = NFSQuota(user, f'/home1/{user}').get()
        self.assertIsNotNone(nfs_quota)
        quota_json = nfs_quota.to_ood_json()
        self.assertIsNotNone(quota_json)
        self.assertEqual(quota_json['user'], user)
        self.assertEqual(quota_json['path'], f'/home1/{user}')
        self.assertIsNotNone(quota_json['total_block_usage'])
        self.assertIsNotNone(quota_json['block_limit'])
        self.assertIsNotNone(quota_json['total_file_usage'])
        self.assertIsNotNone(quota_json['file_limit'])
