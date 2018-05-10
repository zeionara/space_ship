import sys, os
import configparser
import datetime
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from requirement_mapper import RequirementMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import string_to_bytes, parse_timestamp_parameter, parse_objectid_parameter, parse_bytes_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital')

import mongo_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateRequirement(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        content = graphene.String()

    ok = graphene.Boolean()
    requirement = graphene.Field(lambda: RequirementMapper)

    def mutate(self, info, name, content):
        requirement = None
        try:
            requirement = RequirementMapper.init_scalar(mongo_mediator.create_requirement(name, content))
            ok = True
        except IndexError:
            ok = False
        return CreateRequirement(requirement = requirement, ok = ok)

class RemoveRequirement(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    requirement = graphene.Field(lambda: RequirementMapper)

    def mutate(self, info, id):
        requirement = RequirementMapper.init_scalar(mongo_mediator.remove_requirement(id))
        ok = True
        return RemoveRequirement(requirement = requirement, ok = ok)

class UpdateRequirements(graphene.Mutation):
    class Arguments:

        id = graphene.String(default_value = '')
        name = graphene.String(default_value = '')

        set_name = graphene.String(default_value = '')
        set_content = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, name, set_name, set_content):
        try:
            mongo_mediator.update_requirements(_id = parse_objectid_parameter(id), name = name, set_name = set_name, set_content = set_content)
            ok = True
        except IndexError:
            ok = False
        return UpdateRequirements(ok = ok)