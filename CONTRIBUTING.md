# Welcome to VerbaCap contributing

Thank you for investing your time in contributing to our project!

Read our [Code of Conduct](./CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.

## New contributor guide

To get an overview of the project, read the [README](README.md) file. Here are some resources to help you get started with open source contributions:

* [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
* [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
* [Git flow Simple](https://danielkummer.github.io/git-flow-cheatsheet/index.html)
* [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)
* [Commit message guideline](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits)

## Getting started
### Issues

#### Create a new issue

If you spot a problem with the docs, [search if an issue already exists](https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments). If a related issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/github/docs/issues/new/choose).

#### Solve an issue

Scan through our [existing issues](https://github.com/github/docs/issues) to find one that interests you. You can narrow down the search using `labels` as filters. See "[Label reference](https://docs.github.com/en/contributing/collaborating-on-github-docs/label-reference)" for more information. As a general rule, we don’t assign issues to anyone. If you find an issue to work on, you are welcome to open a PR with a fix.

### Make Changes

1. Fork the repository
- Using GitHub Desktop:
  - [Getting started with GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/getting-started-with-github-desktop) will guide you through setting up Desktop.
  - Once Desktop is set up, you can use it to [fork the repo](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/cloning-and-forking-repositories-from-github-desktop)!

- Using the command line:
  - [Fork the repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) so that you can make your changes without affecting the original project until you're ready to merge them.

2. Start psql and redis version used in the using docker-compose file
3. Create `develop.env` file with this content:
```
DATABASE_URL="postgres://YOUR_PSQL_USER:YOUR_PSQL_PWD@PSQL_HOST:PSQL_PORT/PSQL_DB"
DJANGO_SECRET_KEY="GENERATEARANDOMKEY"
DJANGO_DEBUG="True"
CELERY_BROKER_URL="redis://YOUR_REDIS_HOST:6379/0"
PERSIST_AUDIO_ROOTDIR="TEMPORARY_DIRECTORY_TO_STORE_PERSIST"

export DATABASE_URL
export DJANGO_SECRET_KEY
export DJANGO_DEBUG
export CELERY_BROKER_URL
export PERSIST_AUDIO_ROOTDIR
```
4. Create venv using `python3 -m venv .venv`
5. Load all the env files `. ./develop.env && . ./.venv/bin/activate`
6. Install all the requirements using `pip install -r requirements.txt`
7. Install the Git hook using `pre-commit install`
8. Start from develop create a new feature branch using the git flow
9. Start with your changes!
10. Write/update tests for the changes you made, if necessary (coverage 80% or higher).
11. Run the unit test using `coverage run -m pytest`
12. Verify the coverage using `coverage report`
13. Update `README.md` and `CONTRIBUTORS.md`, if necessary.
14. Push the code in your forked repository
15. Open a Pull Request with a comprehensive description of changes.
