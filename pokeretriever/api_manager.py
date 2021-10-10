from aiohttp import ClientSession
import asyncio
from pokeretriever.retriever import Request


class APIManager:
    """
        Manages the JSON request calls to the pokeapi website.
    """

    def create_urls(self, request: Request):
        """
            Returns the url when given the mode by the user
        :param request: Request json
        :return: urls list containing the url
        """

        urls = []
        for r in request.searches:
            urls.append("https://pokeapi.co/api/v2/" + request.mode + "/" + r)
        return urls

    async def get_json(self, url, session):
        """
            Gets the json request.
        :param url: String corresponding to the URL
        :param session: json session
        :return: response.json or none depending on the status
        """

        response = await session.request(method="GET", url=url)
        if response.status == 200: # Only when the status is 200 will we want to get the response.json
            try:
                return await response.json()
            except ValueError as e:
                print(e)
        return None

    async def manage_request(self, request):
        """
            Manages requests made to poke api.
        :param request: json request sent to the server
        :return: results list of asyncio calls
        """
        urls = self.create_urls(request)
        calls = []
        results = []
        json_results = []
        sreuslt = []
        areuslt = []
        mreuslt = []

        async with ClientSession() as session:
            if len(request.stat_urls) > 0:

                # Parsing stats' urls
                for urls in request.stat_urls:
                    for url in urls:
                        calls.append(asyncio.create_task(self.get_json(url, session)))
                        results += await asyncio.gather(*calls)
                        sreuslt.append(results)
                        calls = []
                        results = []
                json_results.append(sreuslt)

                # Parsing ability urls
                for urls in request.ability_urls:
                    for url in urls:
                        calls.append(asyncio.create_task(self.get_json(url, session)))
                        results += await asyncio.gather(*calls)
                        areuslt.append(results)
                        calls = []
                        results = []
                json_results.append(areuslt)

                # Parsing move urls
                for urls in request.move_urls:
                    for url in urls:
                        calls.append(asyncio.create_task(self.get_json(url, session)))
                        results += await asyncio.gather(*calls)
                        mreuslt.append(results)
                        calls = []
                        results = []
                json_results.append(mreuslt)

            else:
                # Groups all urls together from above and returns the appended url list
                for url in urls:
                    calls.append(asyncio.create_task(self.get_json(url, session)))
                    json_results = await asyncio.gather(*calls)

            return json_results
