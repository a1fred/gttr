from urllib.parse import urljoin
import requests


class GitlabApi:
    def __init__(self, url_base: str, token: str) -> None:
        self.url_base = url_base
        self.token = token

    def _request(self, path: str, allow_http_status=(200, )) -> dict:
        headers = {
            "Private-Token": self.token
        }

        resp = requests.get(
            urljoin(self.url_base, path),
            headers=headers,
        )

        if resp.status_code not in allow_http_status:
            raise ValueError(resp.text)
        else:
            return resp.json()

    def projects(self):
        page = 1
        while True:
            pl = self._request('projects?page=%s' % page)
            if not pl:
                break
            else:
                yield from pl
                page += 1

    def issues(self, project_id: int, state='opened'):
        page = 1
        while True:
            pl = self._request('projects/%s/issues?page=%s&state=%s' % (str(project_id), page, state))
            if not pl:
                break
            else:
                yield from pl
                page += 1
    
    def merge_requests(self, project_id: int):
        page = 1
        while True:
            pl = self._request('projects/%s/issues?page=%s&state=all' % (str(project_id), page))
            if not pl:
                break
            else:
                yield from pl
                page += 1

    def merge_requests_notes(self, project_id: int, mr_iid: int):
        page = 1

        while True:
            pl = self._request('projects/%s/issues/%s/notes?page=%s' % (project_id, mr_iid, page))
            if not pl:
                break
            else:
                yield from pl
                page += 1

    def issue_notes(self, project_id: int, issue_iid: int):
        page = 1

        while True:
            pl = self._request('projects/%s/issues/%s/notes?page=%s' % (project_id, issue_iid, page))
            if not pl:
                break
            else:
                yield from pl
                page += 1
