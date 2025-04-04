import os
import glob

from transformers import AutoTokenizer

from config import args
from triplet import TripletDict, EntityDict, Ruledict, LinkGraph
from logger_config import logger
import random

train_triplet_dict: TripletDict = None
all_triplet_dict: TripletDict = None
rule_dict: Ruledict = None
link_graph: LinkGraph = None
entity_dict: EntityDict = None
tokenizer: AutoTokenizer = None


def _init_entity_dict():
    global entity_dict
    if not entity_dict:
        entity_dict = EntityDict(entity_dict_dir=os.path.dirname(args.valid_path))


def _init_train_triplet_dict():
    global train_triplet_dict
    if not train_triplet_dict:
        train_triplet_dict = TripletDict(path_list=[args.train_path], relation_path=args.relation_path, task=args.task)

def _init_rule_dict():
    global rule_dict
    if not rule_dict:
        rule_dict = Ruledict(path=args.rule_path)


def _init_all_triplet_dict():
    global all_triplet_dict
    if not all_triplet_dict:
        path_pattern = '{}/*.txt.json'.format(os.path.dirname(args.train_path))
        all_triplet_dict = TripletDict(path_list=glob.glob(path_pattern), relation_path=args.relation_path, task=args.task)


def _init_link_graph():
    global link_graph
    if not link_graph:
        link_graph = LinkGraph(train_path=args.train_path)


def get_entity_dict():
    _init_entity_dict()
    return entity_dict


def get_train_triplet_dict():
    _init_train_triplet_dict()
    return train_triplet_dict

def get_rule_dict():
    _init_rule_dict()
    return rule_dict


def get_all_triplet_dict():
    _init_all_triplet_dict()
    return all_triplet_dict


def get_link_graph():
    _init_link_graph()
    return link_graph


def build_tokenizer(args):
    global tokenizer
    if tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained(args.pretrained_model)
        special_tokens = {'additional_special_tokens': ['[MASK_h]', '[STRUCT]']}
        tokenizer.add_special_tokens(special_tokens)
        logger.info('Build tokenizer from {}'.format(args.pretrained_model))


def get_tokenizer():
    if tokenizer is None:
        build_tokenizer(args)
    return tokenizer


# def get_neighbor_trpilets(entity, relation, related_entity, num_forward, num_backward):
#     if entity in id2hr:
#         candidate_triplets = list(set(map(tuple, id2hr[entity])) - {(related_entity, relation)})
#         if len(candidate_triplets) >=num_forward:
#             forward_triplets = list(random.sample(candidate_triplets, num_forward))   # entity is the tail in the triplet
#         elif len(candidate_triplets)>0:
#             forward_triplets = list(random.choices(candidate_triplets, k=num_forward))
#         else:
#             forward_triplets = []
#     else:
#         forward_triplets = []
#     if entity in id2rt:
#         candidate_triplets = list(set(map(tuple, id2rt[entity])) - {(relation, related_entity)})
#         if len(candidate_triplets) >=num_backward:
#             backward_triplets = list(random.sample(candidate_triplets, num_backward))
#         elif len(candidate_triplets) > 0:
#             backward_triplets = list(random.choices(candidate_triplets, k=num_backward))
#         else:
#             backward_triplets = []
#     else:
#         backward_triplets = []
#
#     return forward_triplets, backward_triplets