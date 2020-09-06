from requests_html import AsyncHTMLSession
from time import time, sleep
from typing import Dict, List


class Orunmila:
    def __init__(self, gitlabAddress: str) -> None:
        self._orunSession = AsyncHTMLSession()
        self._gitlabAddress = gitlabAddress

        # do not stop the loop on self.getAllProjectMetadata()
        self._dontStopLoop = True
        self._pagesCount = 0

        # **start** Orunmila knows
        self.projectsMetadata = list()
        self._commitsByYear = dict()
        self._numberOfProjects = 0
        # **end## Orunmila knows

    #

    async def _getProjectMetadata(self) -> None:
        gitlabPlatResponse = await self._orunSession.get(
            f"{self._gitlabAddress}/api/v4/projects?&per_page=100&page={self._pagesCount}"
        )

        if gitlabPlatResponse.json() == []:
            self._dontStopLoop = False
            return
        #

        for pMetadata in gitlabPlatResponse:
            self.projectsMetadata.append(pMetadata)
        #
        # print(self._pagesCount)
        self._pagesCount += 1

    #

    def getAllProjectMetadata(self) -> List:
        while self._dontStopLoop:
            self._orunSession.run(self._getProjectMetadata)
        #
        print(len(self.projectsMetadata))

        # cleanup
        self._pagesCount = 0
        self._dontStopLoop = True

        return self.projectsMetadata

    #

    def getCommitsByYear(self) -> Dict:
        pass

    #


if __name__ == "__main__":
    orun = Orunmila("https://invent.kde.org")
    orun.getAllProjectMetadata()
    orun.projectsMetadata[0]
