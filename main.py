from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI

from schema.hello import resolve_hello

query = QueryType()

# リゾルバー関数を登録
query.set_field("hello", resolve_hello)

type_defs = """
    type Query {
        hello(name: String): String!
    }
"""

schema = make_executable_schema(type_defs, query)

app = FastAPI()
app.add_route("/", GraphQL(schema, debug=True))
