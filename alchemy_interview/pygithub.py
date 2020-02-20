import sys
sys.path.append("./PyGithub");
from github import Github
from githubmodels import Repo, Org, User

import getpass

# Authenticate to github.com and create PyGithub "Github" object
# username = input("Github Username:")
username = "lingtongsun@gmail.com"
pw = getpass.getpass()
g = Github(username, pw)

# Use the PyGithub Github object g to do whatever you want,
# for example, list all your own repos (user is whichever user authenticated)


def get_count(list):
    count = 0
    for i in list:
        count += 1
        # print(count)
        if count > 1000:
            break
    return count

name = "stanford-futuredata"
def get_stats(org_name):
    org_model = Org()
    org = g.get_organization(org_name)
    num_repos = org.public_repos
    print(num_repos)

    repos = org.get_repos()

    count = 0
    for repo in repos:
        count += 1
        if count == 2:
            continue
        if count == 4:
            break
        repo_model = Repo()
        print(repo.name)

        repo_model.stars = repo.stargazers_count
        contributors = repo.get_contributors()
        repo_model.contributors = get_count(contributors)
        for contributor in contributors:
            print(contributor.id)
            u = User(contributor.id)
            if not org_model.users.__contains__(u.id):
                org_model.users[contributor.id] = u

        commits = repo.get_commits()
        repo_model.commits = get_count(commits)

        for commit in commits:
            # print(commit)
            commit_user = commit.author
            if commit_user is None:
                commit_user = commit.committer
            if commit_user is None or org_model.users[commit_user.id] is None:
                raise Exception("Parsing error")

            org_model.users[commit_user.id].commits += 1

        open_pulls = repo.get_pulls(state="open")
        closed_pulls = repo.get_pulls(state="closed")
        repo_model.open_prs = get_count(open_pulls)
        repo_model.closed_prs = get_count(closed_pulls)

        print(repo_model)
        org_model.repos.append(repo_model)

    print(org_model)

get_stats(name)