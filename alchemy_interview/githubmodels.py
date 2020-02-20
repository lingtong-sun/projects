

class Repo:
    def __init__(self):
        self.stars = 0
        self.commits = 0
        self.contributors = 0
        self.open_prs = 0
        self.closed_prs = 0
        self.org = None
        self.name = None

    def __str__(self):
        return "Stars: " + str(self.stars) +"\n" + \
               "Commits: " + str(self.commits) + "\n" + \
               "Contributors: " + str(self.contributors) + "\n" + \
               "Open PRS: " + str(self.open_prs) + "\n" + \
               "Closed PRS: " + str(self.closed_prs) + "\n"


class User:
    def __init__(self, id):
        self.commits = 0
        self.open_prs = 0
        self.closed_prs = 0
        self.id = id

    def __str__(self):
        return str(self.id) + "===> Commits: " + str(self.commits) + ", Open PRS: " + \
               str(self.open_prs) + ", Close PRs: " + str(self.closed_prs)


class Org:
    def __init__(self):
        self.repos = []
        self.users = {}

    def get_stars(self):
        count = 0
        for repo in self.repos:
            count += repo.stars
        return count

    def get_commits(self):
        count = 0
        for repo in self.repos:
            count += repo.commits
        return count

    def get_contributors(self):
        return len(self.users)

    def get_open_prs(self):
        count = 0
        for repo in self.repos:
            count += repo.open_prs
        return count

    def get_closed_prs(self):
        count = 0
        for repo in self.repos:
            count += repo.closed_prs
        return count

    def __str__(self):
        result = ""
        result = "Stars: " + str(self.get_stars()) +"\n" + \
               "Commits: " + str(self.get_commits()) + "\n" + \
               "Contributors: " + str(self.get_contributors()) + "\n" + \
               "Open PRS: " + str(self.get_open_prs()) + "\n" + \
               "Closed PRS: " + str(self.get_closed_prs()) + "\n" + \
               "Users ====================\n"

        for email, user in self.users.items():
            result += user.__str__() + "\n"

        return result