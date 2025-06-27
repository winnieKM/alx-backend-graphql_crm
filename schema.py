# alx-backend-graphql_crm/schema.py
import graphene
from crm.schema import Query, Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
