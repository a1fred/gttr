from itertools import chain
import argparse

from halo import Halo

from gttr.lib.gitlab import GitlabApi
from gttr.timetracking import TimeReport


def main(url_base, token):
    api = GitlabApi(url_base, token)
    tr = TimeReport()

    for p in api.projects():
        with Halo(text='Processing %s' % p['path_with_namespace'], spinner='dots') as spinner:
            # Parse issue times
            for issue in chain(api.issues(project_id=p['id']), api.issues(project_id=p['id'], state='closed')):
                for note in api.issue_notes(project_id=p['id'], issue_iid=issue['iid']):
                    tr.parse_note(note['author']['username'], note['body'], note['created_at'])

            # Parse merge requests times
            for mr in api.merge_requests(project_id=p['id']):
                for note in api.merge_requests_notes(project_id=p['id'], mr_iid=mr['iid']):
                    tr.parse_note(note['author']['username'], note['body'], note['created_at'])

            spinner.succeed()

    for u, s in tr.total_report():
        print("👨  %s spent: %s hrs" % (u, int(s / 3600)))


def cli():
    parser = argparse.ArgumentParser("Gitlab timetrackin reporter")
    parser.add_argument('url_base')
    parser.add_argument('token')
    main(**vars(parser.parse_args()))
