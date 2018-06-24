#
# from rest_framework import response
# # noinspection PyArgumentList
# @api_view()
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
# def schema_view(request):
#     print("---inside schema view-----")
#     # noinspection PyArgumentList
#     schema = coreapi.Document(
#     title='Your Title',
#     url='Your host url',
#     content={
#         'search': coreapi.Link(
#             url='/search/',
#             action='post',
#             fields=[
#                 coreapi.Field(
#                     name='search',
#                     required=True,
#                     location='query',
#                     description='Any Person Name or Movie Name'
#                 )
#             ],
#             description='Search field.'
#         )
#     }
# )
#     # schema = generator.get_schema(request)
#     return response.Response(schema)