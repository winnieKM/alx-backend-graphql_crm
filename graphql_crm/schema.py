import graphene
from crm.schema import Mutation, Query as CrmQuery

class Query(CrmQuery, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query, mutation=Mutation)
