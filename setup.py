from setuptools import setup, find_packages

setup(
    name='mkdocs-github-contributors-plugin',
    version='0.1',
    packages=find_packages(),
    url="https://github.com/rippedpiracy/mkdocs-github-contributors-plugin",
    license="GPL3",
    author="rippedpiracy",
    keywords="mkdocs",
    description="MkDocs plugin to show GitHub contributors",
    long_description="MkDocs plugin to show GitHub contributors",
    entry_points={
        'mkdocs.plugins': [
            'github-contributors = mkdocs_github_contributors_plugin.plugin:GitHubContributorsPlugin',
        ]
    }
)
