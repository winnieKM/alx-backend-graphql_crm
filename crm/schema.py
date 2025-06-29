import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from decimal import Decimal

# ---------- Types ----------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

# ---------- Inputs ----------
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int()

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)

# ---------- Mutations ----------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        try:
            validate_email(input.email)
            if Customer.objects.filter(email=input.email).exists():
                raise Exception("Email already exists")
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone or ""
            )
            return CreateCustomer(customer=customer, message="Customer created successfully")
        except ValidationError:
            raise Exception("Invalid email format")
        except Exception as e:
            raise Exception(str(e))

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []
        for data in input:
            try:
                validate_email(data.email)
                if Customer.objects.filter(email=data.email).exists():
                    raise Exception(f"Email {data.email} already exists")
                customer = Customer.objects.create(
                    name=data.name,
                    email=data.email,
                    phone=data.phone or ""
                )
                customers.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive")
        stock = input.stock if input.stock is not None else 0
        if stock < 0:
            raise Exception("Stock must be non-negative")
        product = Product.objects.create(
            name=input.name,
            price=Decimal(input.price),
            stock=stock
        )
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer does not exist")

        products = Product.objects.filter(id__in=input.product_ids)
        if not products.exists():
            raise Exception("No valid products found")

        total_amount = sum(p.price for p in products)

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount
        )
        order.products.set(products)

        return CreateOrder(order=order)

# ---------- Root Mutation ----------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

# ---------- Optional Query ----------
class Query(graphene.ObjectType):
    ping = graphene.String()

    def resolve_ping(self, info):
        return "pong"
