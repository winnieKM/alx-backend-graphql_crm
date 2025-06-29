import graphene
from crm.schema import Query as CrmQuery
from crm.schema import Mutation as CrmMutation

class Query(CrmQuery, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

class Mutation(CrmMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
