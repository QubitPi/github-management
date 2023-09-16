# Copyright Jiaqi Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import os
import requests

if __name__ == '__main__':
    # https://stackoverflow.com/a/7427376
    parser = argparse.ArgumentParser(description='Delete all labels of a GitHub Repo')
    parser.add_argument('-o', '--owner', help='Repository owner', required=True)
    parser.add_argument('-r', '--repo', help='Repository name', required=True)
    args = vars(parser.parse_args())

    repo_owner = args["owner"]
    repo_name = args["repo"]

    headers = {
        'Accept': 'application/vnd.github+json',
        "Authorization": "Bearer " + os.environ['GITHUB_MANAGEMENT_TOKEN']
    }

    url = "https://api.github.com/repos/{repo_owner}/{repo_name}/labels".format(repo_owner=repo_owner, repo_name=repo_name)
    for label_url in [label["url"] for label in requests.get(url, headers=headers).json()]:
        requests.delete(label_url, headers=headers)
