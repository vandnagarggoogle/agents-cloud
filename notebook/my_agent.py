class MyAgent:
    def query_none(self, message: dict = None, **kwargs):
        return None

    def query_dict(self, f: str = "default", to: str = "default", message: dict = None, **kwargs):
        return {"from": f, "to": to}

    def query_int(self, message: dict = None, **kwargs):
        return 5

    def query_str(self, message: dict = None, **kwargs):
        return "str"

    def query_bool(self, message: dict = None, **kwargs):
        return True

    def query_list(self, message: dict = None, **kwargs):
        return [1, 2, 3]

    def query_dict_list(self, message: dict = None, **kwargs):
        return [{"a": 1}, {"b": 2}]

    async def async_query_none(self, message: dict = None, **kwargs):
        return None

    async def async_query_dict(self, f: str = "default", to: str = "default", message: dict = None, **kwargs):
        return {"from": f, "to": to}

    async def async_query_int(self, message: dict = None, **kwargs):
        return 5

    async def async_query_str(self, message: dict = None, **kwargs):
        return "str"

    async def async_query_bool(self, message: dict = None, **kwargs):
        return True

    async def async_query_list(self, message: dict = None, **kwargs):
        return [1, 2, 3]

    async def async_query_dict_list(self, message: dict = None, **kwargs):
        return [{"a": 1}, {"b": 2}]

    def stream_query(self, f: str = "default", to: str = "default", message: dict = None, **kwargs):
        yield self.query_none()
        yield self.query_int()
        yield self.query_str()
        yield self.query_bool()
        yield self.query_list()
        yield self.query_dict_list()
        yield self.query_dict(f, to)

    async def async_stream_query(self, message: dict = None, f: str = "default", to: str = "default", **kwargs):
        """
        The Playground calls this method and passes a 'message' object containing the user prompt.
        """
        # Extract user input from the Playground's message format
        user_input = message['parts'][0]['text'] if message else "No input provided"
        
        yield f"Echo from Agent: You said '{user_input}'. "
        yield f"Parameters used: from={f}, to={to}. "
        
        # Simulating processing
        yield "Processing synchronous steps... "
        result = await self.async_query_str()
        yield f"Internal result: {result}. "
        yield "Query complete!"

    def register_operations(self):
        return {
            "": [
                "query_none", "query_int", "query_str", "query_bool", "query_list",
                "query_dict_list", "query_dict",
            ],
            "async": [
                "async_query_none", "async_query_int", "async_query_str",
                "async_query_bool", "async_query_list", "async_query_dict_list",
                "async_query_dict",
            ],
            "stream": ["stream_query"],
            "async_stream": ["async_stream_query"],
        }

# This must be named 'agent' to match your entrypoint_object
agent = MyAgent()
