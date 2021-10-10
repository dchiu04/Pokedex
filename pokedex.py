import asyncio
from pokeretriever.retriever import Request, RequestManager
from pokeretriever.retriever import RequestHandler


class Pokedex:
    """
    Driver class that sets up chains of responsibility.
    """

    def __init__(self):
        self._handler = RequestHandler()

    async def execute_request(self, request: Request):
        await self._handler.handle_request(request)


def main():
    request = RequestManager.parse_arguments_to_request()
    pokedex = Pokedex()

    try:
        asyncio.run(pokedex.execute_request(request))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
