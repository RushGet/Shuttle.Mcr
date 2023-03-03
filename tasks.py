import re
import yaml
from invoke import task
import logging


def load_config():
    # Load config from file
    path = "config/config.yaml"
    with open(path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def select_mcr_tags(config, mcr_tags_json):
    image_name = mcr_tags_json['name']
    # find image selector from config where selector[].image match mar_tags_json.name
    image_selector_config = [x for x in config['selectors'] if (x['image'] == image_name and x['type'] == 'mcr')]
    if len(image_selector_config) == 0:
        logging.warning(f"No image selector found for image: {image_name}")
        return None
    elif len(image_selector_config) > 1:
        logging.warning(f"Multiple image selectors found for image: {image_name}")
        return None
    else:
        image_selector_config = image_selector_config[0]
        # test each tags in mcr_tags_json.tags by selector[].tag_regex and selector[].tag_regex_exclude
        # if tag_regex is not defined, all tags are selected
        # if tag_regex_exclude is defined, tags matching tag_regex_exclude are excluded
        results = []
        for tag in mcr_tags_json['tags']:
            if 'tag_regex' in image_selector_config:
                for tag_regex in image_selector_config['tag_regex']:
                    if re.match(tag_regex, tag):
                        if 'tag_regex_exclude' in image_selector_config:
                            for tag_regex_exclude in image_selector_config['tag_regex_exclude']:
                                if re.match(tag_regex_exclude, tag):
                                    break
                            else:
                                results.append(tag)
                        else:
                            results.append(tag)
                        break
        return results


@task
def hello(c):
    config = load_config()
    print(config)
