import unittest

from tasks import *


class MyTestCase(unittest.TestCase):
    def test_load_config(self):
        config = load_config()
        self.assertIsNotNone(config)
        self.assertEqual(config.version, 0.1)
        print(config)

    def test_filter_by_tag_selectors(self):
        config = load_config()
        with open('test_data/dotnet_sdk_tags.json', "r", encoding='utf-8') as f:
            mcr_tags_json = json.load(f)
        result = select_mcr_tags(config.images[0], mcr_tags_json['tags'])
        self.assertIsNotNone(result)
        with open('test_data/dotnet_sdk_match_data.json', "r", encoding='utf-8') as f:
            match_data = json.load(f)
        print(result[0])
        # check tags
        self.assertEqual(result[0].tags, match_data)

    def test_filter_by_tag_selectors_redis(self):
        config = load_config()
        with open('test_data/redis_dockerhub_tags.json', "r", encoding='utf-8') as f:
            mcr_tags_json = json.load(f)
        result = select_mcr_tags(config.images[1], mcr_tags_json['tags'])
        print(result)
        self.assertIsNotNone(result)
        with open('test_data/redis_match_data.json', "r", encoding='utf-8') as f:
            match_data = json.load(f)
        print(result[0])
        # check tags
        self.assertEqual(result[0].tags, match_data)


class McrTagMatchTests(unittest.TestCase):
    def test_match_include(self):
        tag = '3.1.201'
        regex_list = ['^3\\..*']
        regex_exclude_list = None
        self.assertTrue(match_tag_by_regex(tag, regex_list, regex_exclude_list))

    def test_match_exclude(self):
        tag = '3.1.201-preview1'
        regex_list = ['^3\\..*']
        regex_exclude_list = ['.*preview.*']
        self.assertFalse(match_tag_by_regex(tag, regex_list, regex_exclude_list))


class ImageSyncDataTests(unittest.TestCase):
    def test_create_image_sync_data_json(self):
        items = [
            ImageTransportation('mcr.microsoft.com',
                                'dotnet/sdk',
                                'registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk',
                                ['3.1.201', '3.1.202'])]
        result = create_image_sync_data_json(items)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        expected = {
            "mcr.microsoft.com/dotnet/sdk:3.1.201": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:3.1.201",
            "mcr.microsoft.com/dotnet/sdk:3.1.202": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:3.1.202"
        }
        self.assertEqual(expected, result[0].items)
        self.assertEqual('dotnet_sdk-0', result[0].name)
        logging.info(result[0])

    def test_create_image_sync_data_json_with_more_tags(self):
        items = [
            ImageTransportation('mcr.microsoft.com',
                                'dotnet/sdk',
                                'registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk',
                                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])]
        result = create_image_sync_data_json(items)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        expected0 = {
            "mcr.microsoft.com/dotnet/sdk:1": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:1",
            "mcr.microsoft.com/dotnet/sdk:2": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:2",
            "mcr.microsoft.com/dotnet/sdk:3": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:3",
            "mcr.microsoft.com/dotnet/sdk:4": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:4",
            "mcr.microsoft.com/dotnet/sdk:5": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:5",
            "mcr.microsoft.com/dotnet/sdk:6": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:6",
            "mcr.microsoft.com/dotnet/sdk:7": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:7",
            "mcr.microsoft.com/dotnet/sdk:8": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:8",
            "mcr.microsoft.com/dotnet/sdk:9": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:9",
            "mcr.microsoft.com/dotnet/sdk:10": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:10"
        }
        self.assertEqual(result[0].items, expected0)

        expected1 = {
            "mcr.microsoft.com/dotnet/sdk:11": "registry.cn-hangzhou.aliyuncs.com/newbe36524/dotnet-sdk:11"
        }
        self.assertEqual(result[1].items, expected1)


if __name__ == '__main__':
    unittest.main()
