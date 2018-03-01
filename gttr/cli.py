from itertools import chain
import argparse

from halo import Halo

from gttr.lib.gitlab import GitlabApi
from gttr.timetracking import TimeReport


def main(url_base, token, projects):
    api = GitlabApi(url_base, token)
    tr = TimeReport()

    if projects is None:
        projects_iterator = api.projects()
    else:
        projects_iterator = [p for p in api.projects() if p['path_with_namespace'] in projects]

    for p in projects_iterator:
        with Halo(text='Processing %s' % p['path_with_namespace'], spinner='dots') as spinner:
            # Parse issue times
            for issue in chain(api.issues(project_id=p['id']), api.issues(project_id=p['id'], state='closed')):
                if issue['time_stats']['total_time_spent'] != 0:
                    for note in api.issue_notes(project_id=p['id'], issue_iid=issue['iid']):
                        tr.parse_note(note['author']['username'], note['body'], note['created_at'])

            # Parse merge requests times
            for mr in api.merge_requests(project_id=p['id']):
                if mr['time_stats']['total_time_spent'] != 0:
                    for note in api.merge_requests_notes(project_id=p['id'], mr_iid=mr['iid']):
                        tr.parse_note(note['author']['username'], note['body'], note['created_at'])

            spinner.succeed()

    print("\nTotal report:")
    for u, s in tr.total_report():
        print("👨  %s spent: %sh" % (u, int(s / 3600)))


def cli():
    parser = argparse.ArgumentParser("Gitlab timetracking reporter")
    parser.add_argument('url_base')
    parser.add_argument('token')
    parser.add_argument('projects', nargs='*')
    main(**vars(parser.parse_args()))
