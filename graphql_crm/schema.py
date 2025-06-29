import graphene

class Query(graphene.ObjectType):

    hello = graphene.String(default_value="Hello, GraphQL!")

    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)
