class MyAgent:

  def query_none(self):
    return None

  def query_dict(self, f: str, to: str):
    return {"from": f, "to": to}

  def query_int(self):
    return 5

  def query_str(self):
    return "str"

  def query_bool(self):
    return True

  def query_list(self):
    return [1, 2, 3]

  def query_dict_list(self):
    return [{"a": 1}, {"b": 2}]

  async def async_query_none(self):
    return None

  async def async_query_dict(self, f: str, to: str):
    return {"from": f, "to": to}

  async def async_query_int(self):
    return 5

  async def async_query_str(self):
    return "str"

  async def async_query_bool(self):
    return True

  async def async_query_list(self):
    return [1, 2, 3]

  async def async_query_dict_list(self):
    return [{"a": 1}, {"b": 2}]

  def stream_query(self, f: str, to: str):
    yield self.query_none()
    yield self.query_int()
    yield self.query_str()
    yield self.query_bool()
    yield self.query_list()
    yield self.query_dict_list()
    yield self.query_dict(f, to)

  async def async_stream_query(self, f: str, to: str):
    result = await self.async_query_none()
    yield result
    result = await self.async_query_int()
    yield result
    result = await self.async_query_str()
    yield result
    result = await self.async_query_bool()
    yield result
    result = await self.async_query_list()
    yield result
    result = await self.async_query_dict_list()
    yield result
    result = await self.async_query_dict(f, to)
    yield result

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

agent = MyAgent()