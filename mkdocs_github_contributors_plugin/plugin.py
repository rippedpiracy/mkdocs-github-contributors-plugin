#!/usr/bin/python3

import requests
import re

from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import PluginError
from mkdocs.config import config_options

item_formatting = """\
<td class=\"contributor-item\">
    <a href="https://github.com/{username}" title="{username}" class=\"contributor\" target="_blank">
        <img src="{avatar_url}">
        <br />
        <b>{username}</b>
    </a>
</td>\n"""

class GitHubContributorsPlugin(BasePlugin):

    config_scheme = (
        ('repository', config_options.Type(str, default='')),
        ('clientId', config_options.Type(str, default='')),
        ('clientSecret', config_options.Type(str, default='')),
        ('contributorsFile', config_options.Type(str, default='')),
        ('excludedIds', config_options.Type(list, default=[])),
    )

    def __init__(self):
        self.formatted_contributors = ""

    def _get_custom_contributors(self):
        with open(self.config['contributorsFile'], 'r') as fin:
            for line in fin:
                fline = line.split('/')
                login = fline[0]
                userId = fline[1]
                self._data.append({
                    'login': login,
                    'avatar_url': 'https://avatars.githubusercontent.com/u/{}'.format(userId)
                })
            

    def _get_data(self):
        try:
            if self.config['clientId'] != "" and self.config['clientSecret'] != "":
                response = requests.get("https://api.github.com/repos/{}/contributors".format(self.config['repository']), auth=(self.config['clientId'], self.config['clientSecret']))
            else:
                response = requests.get("https://api.github.com/repos/{}/contributors".format(self.config['repository']))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise PluginError(str(e))

        self._data = response.json()

        # remove excluded contributors
        self._data = [x for x in self._data if x['id'] not in self.config['excludedIds']]

        if self.config['contributorsFile'] != '':
            self._get_custom_contributors()
        self.formatted_contributors = "<table class=\"contributors-github\">\n"
        i = 0
        inRow = False
        while i < len(self._data):
            if i%4 == 0 and inRow == False:
                self.formatted_contributors += "<tr>\n"
                inRow = True
            elif i%4 == 0 and inRow == True:
                self.formatted_contributors += "</tr>\n"
                inRow = False
            contributor = self._data[i]
            self.formatted_contributors += item_formatting.format(username=contributor['login'], avatar_url=contributor['avatar_url'])
            i += 1
        if inRow == True:
            self.formatted_contributors += "</tr>\n"
        self.formatted_contributors += "</table>"


    def on_page_markdown(self, markdown, page=None, config=None, **kwargs):
        if "{{ github.contributors }}" in markdown:
            if self.formatted_contributors == "":
                self._get_data()
            return markdown.replace("{{ github.contributors }}", self.formatted_contributors)
        else:
            return markdown
