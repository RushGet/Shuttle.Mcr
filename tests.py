import json
import unittest

from tasks import load_config, select_mcr_tags


class MyTestCase(unittest.TestCase):
    def test_load_config(self):
        config = load_config()
        self.assertIsNotNone(config)
        self.assertEqual(config['version'], 0.1)
        print(config)

    def test_filter_by_tag_selectors(self):
        config = load_config()
        with open('test_data/dotnet_sdk_tags.json', "r", encoding='utf-8') as f:
            mcr_tags_json = json.load(f)
        tags = select_mcr_tags(config, mcr_tags_json)
        self.assertIsNotNone(tags)
        with open('test_data/dotnet_sdk_match_data.json', "r", encoding='utf-8') as f:
            match_data = json.load(f)
        self.assertEqual(tags, match_data)


if __name__ == '__main__':
    unittest.main()
