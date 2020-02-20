from github import Github
import requests

org = "bitcoin"
base_url = "https://api.github.com/"

class Repo:
    def __init__(self):
        self.stars = 0
        self.commits = 0
        self.contributors = 0
        self.open_prs = 0
        self.closed_prs = 0
        self.org = None
        self.name = None



def get_stats(org):

    # get org info
    response = requests.get(url=base_url + "orgs/" + org)
    if not response.ok:
        raise Exception("Error getting org info.")
    org_json = response.json()

    num_repos = org_json['public_repos']
    repos = {}
    repos_url = org_json['repos_url']

    print(repos_url)
    repo_response = requests.get(url=repos_url)

    repos_json = repo_response.json()

    # for each repo
    for i in range(0, num_repos):
        repos[i] = Repo()
        repos[i].stars = repos_json[i]['stargazers_count']

        commits_url = base_url + "repos/" + repos_json[i]['full_name'] + "/commits"
        print(commits_url)
        commits_json = requests.get(url=commits_url).json()
        print(commits_json[0])
        print(len(commits_json))



    print(num_repos)


get_stats(org)