# mkdocs-github-contributors-plugin

Plugin for [MkDocs](https://mkdocs.org). Inserts a list of GitHub contributors.

## Installation

```
pip install mkdocs-github-contributors-plugin
```

## Configuration

```yaml
plugins:
  - github-contributors:
      repository: <repo>
      contributorsFile: <contributorsFile>
      excludedIds:
        - <id>

      # optional
      clientId: <clientId>
      clientSecret: <clientSecret>
```

- `repository`: should be in the form `${owner}/${repo}`

- `clientId` and `clientSecret` are not required, but increase the GitHub API ratelimit
