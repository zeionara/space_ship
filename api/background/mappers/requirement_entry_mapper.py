import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

from specialization_mapper import SpecializationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class RequirementEntryMapper(graphene.ObjectType):
    
    specialization = graphene.Field(lambda: SpecializationMapper)
    quantity = graphene.Int()

    def resolve_specialization(self, info):
    	return SpecializationMapper.init_scalar(mongo_mediator.get_specialization_by_id(self.specialization))

    @staticmethod
    def init_scalar(item):
    	return RequirementEntryMapper(specialization = item['specialization'], quantity = item['quantity'])
