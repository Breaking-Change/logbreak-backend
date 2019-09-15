import requests
import os
import json
import re

def releases(request):
    headers = {'Authorization': os.getenv('GITHUB_TOKEN', '')}
    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            return {'error': 'Github API error'}
    
    path = request.path
    path_parts = path.split('/')
    if len(path_parts) != 3:
        return '{"error": "Bad request"}'
    else:
        _, repo_owner, repo_name = path_parts
        query_head = f'{{ repository(owner: \"{repo_owner}\", name: \"{repo_name}\") {{'
        query_tail = '''
            releases(last: 100) {
              edges {
                node {
                tagName
                description
                }
              }
            }
          }
        }
        '''

        query = query_head + query_tail

        query_resp = run_query(query)
        nodes = query_resp['data']['repository']['releases']['edges']
        pattern = re.compile(r'[^\d]*(\d+\.\d[\d\.]+)[^\d]*')
        prev_major_version = None
        breaking_releases = []
        seen_major_versions = set()
        for node in nodes:

            node = node['node']
            tag_name = node['tagName']
            version = re.match(pattern, tag_name)[1]
            major_version = int(version.split('.')[0])
            if (prev_major_version is not None and prev_major_version < major_version and major_version not in seen_major_versions) or (re.search('breaking change', node['description'], re.IGNORECASE)):
                breaking_releases.append(node)
                seen_major_versions.add(major_version)
            prev_major_version = major_version
        return json.dumps(breaking_releases)
