from requests_html import AsyncHTMLSession
from typing import Dict, List
from json import dumps


class Orunmila:
    def __init__(self, gitlabAddress: str) -> None:
        self._orunSession = AsyncHTMLSession()
        self._gitlabAddress = gitlabAddress

        # do not stop the loop on self.getAllProjectMetadata()
        self._dontStopLoop = True
        self._pagesCount = 0

        # raw data
        self.projectsMetadata = list()
        self.projectCommitsMetadata = list()

        # **start** Orunmila knows
        self._commitsByYear = dict()
        self._numberOfProjects = 0
        # **end## Orunmila knows

    #

    # secondary method
    async def _getProjectMetadata(self) -> None:
        gitlabPlatResponse = await self._orunSession.get(
            f"{self._gitlabAddress}/api/v4/projects?&per_page=100&page={self._pagesCount}"
        )

        if gitlabPlatResponse.json() == []:
            self._dontStopLoop = False
            return
        #

        for pMetadata in gitlabPlatResponse.json():
            self.projectsMetadata.append(dict(pMetadata))
        #
        self._pagesCount += 1

    #

    # secondary method
    async def _getCommitsMetadata(self) -> None:
        pageCount = 0
        gitlabPlatResponse = await self._orunSession.get(
            f"{self._gitlabAddress}/api/v4/projects/{self._projectCurrentTd}/repository/commits?&per_page=100&page={pageCount}"
        )
        while gitlabPlatResponse.json() != []:
            tmp_gitlabPlatResponse = gitlabPlatResponse.json()
            for pCommit in tmp_gitlabPlatResponse:
                try:
                    self.projectCommitsMetadata.append(dict(pCommit))
                except ValueError as error:
                    print(
                        f"Error getting commits: {error}, on repository id: {self._projectCurrentTd}"
                    )
                #
            #
            pageCount += 1
            gitlabPlatResponse = await self._orunSession.get(
                f"{self._gitlabAddress}/api/v4/projects/{self._projectCurrentTd}/repository/commits?&per_page=100&page={pageCount}"
            )
        #
        print(f"getting data of project {self._projectCurrentTd}")

    #

    def getAllProjectsMetadata(self) -> List:
        while self._dontStopLoop:
            self._orunSession.run(self._getProjectMetadata)
        #
        print(len(self.projectsMetadata))

        # cleanup
        self._pagesCount = 0
        self._dontStopLoop = True

        return self.projectsMetadata

    #

    def getAllCommitsMetadata(self) -> List:
        for project in self.projectsMetadata:
            self._projectCurrentTd = project["id"]
            self._orunSession.run(self._getCommitsMetadata)
        #

        # cleanup
        del self._projectCurrentTd

        return self.projectCommitsMetadata

    #


if __name__ == "__main__":
    orun = Orunmila("https://invent.kde.org")
    orun.getAllProjectsMetadata()
    orun.getAllCommitsMetadata()
    # orun.projectsMetadata[0]
