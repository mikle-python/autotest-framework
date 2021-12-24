import json
from libs.request_obj import RequstObj
from urllib.parse import urljoin
from libs.log_obj import LogObj


class HarborObj(RequstObj):
    def __init__(self, registry):
        super(HarborObj, self).__init__()
        self.registry = registry
        self.harbor_url = 'https://{0}/api/v2.0/'.format(registry)

    def get_repositories_by_project(self, project_name):
        i = 1
        all_repositories = []
        while True:
            url = urljoin(self.harbor_url, 'projects/{0}/repositories?page={1}&page_size=10'.format(project_name, i))
            response = self.call('get', url)
            if response.status_code == 200:
                repositories = json.loads(response.text)
                if len(repositories) > 0:
                    all_repositories.extend(repositories)
                    i = i + 1
                else:
                    break
            else:
                raise Exception('Get repositories fail, error is {0}!'.format(response.text))
        return all_repositories

    def get_artifacts_by_repository(self, project_name, repository_name):
        i = 1
        all_artifacts = []
        while True:
            url = urljoin(self.harbor_url, 'projects/{0}/repositories/{1}/artifacts?page={2}&page_size=10'
                                           '&with_tag=true&with_label=false&with_scan_overview=false'
                                           '&with_signature=false&with_immutable_status=false'.format(project_name,
                                                                                                      repository_name,
                                                                                                      i))
            response = self.call('get', url)
            if response.status_code == 200:
                artifacts = json.loads(response.text)
                if len(artifacts) > 0:
                    all_artifacts.extend(artifacts)
                    i = i + 1
                else:
                    break
            else:
                raise Exception('Get repositories fail, error is {0}!'.format(response.text))
            break
        return all_artifacts

    def get_tag(self, project_name, repository_name):
        artifacts = self.get_artifacts_by_repository(project_name, repository_name)
        latest_artifact = artifacts[0]
        tag_name = latest_artifact['tags'][0]['name']
        # image = '{0}/{1}/{2}:{3}'.format(self.registry, project_name, repository_name, tag_name)
        return tag_name


if __name__ == '__main__':
    harbor_obj = HarborObj('registry.ghostcloud.cn')
    tag_name = harbor_obj.get_tag('arm64v8', 'nginx')
    print(tag_name)
