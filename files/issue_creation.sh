#!/bin/bash

REPO_OWNER="github-gk-aks"
REPO_NAME="post-migration-self-service"
ISSUE_TITLE="Get Repo Size - 4 Repos"
ISSUE_BODY='{
    "firstgithubrepo": {
        "repository": "firstgithubrepo",
        "organisation": "github-gk-aks"
    },
    "secondgithubrepo": {
        "repository": "secondgithubrepo",
        "organisation": "github-gk-aks"
    },
    "thirdgithubrepo": {
        "repository": "thirdgithubrepo",
        "organisation": "github-gk-aks"
    },
    "fourthgithubrepo": {
        "repository": "fourthgithubrepo",
        "organisation": "github-gk-aks"
    }
}'
ISSUE_LABEL="get-repo-size"

gh issue create --repo "$REPO_OWNER/$REPO_NAME" --title "$ISSUE_TITLE" --body "$ISSUE_BODY" --label "$ISSUE_LABEL"
