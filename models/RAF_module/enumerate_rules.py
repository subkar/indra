from pysb import ANY, Parameter
import re
import itertools as it
import copy


def get_reactants(rule):
    ''' Get list of monomers on left-hand side of rule ''' 
    if len(rule.reactant_pattern.complex_patterns) == 2:
        reactants = rule.reactant_pattern.complex_patterns
    elif len(rule.reactant_pattern.complex_patterns) == 1:
        reactants = rule.reactant_pattern.complex_patterns[0].monomer_patterns

    return reactants


def get_products(rule):
    ''' Get list of monomers on right-hand side of rule '''
    if len(rule.product_pattern.complex_patterns) == 1:
        products = rule.product_pattern.complex_patterns[0].monomer_patterns
    elif len(rule.product_pattern.complex_patterns) == 2:
        products = rule.product_pattern.complex_patterns

    return products


def enumerate_rules(model, rule, exclude=[]):
    ''' Given a rule, generate rules for all possible combinations, 
    taking into account the binding sites and occupancy for each
    participating monomer in the rule. '''
    
    reactants = get_reactants(rule)
    reactant_names = [re.split('\(', i.__str__())[0] for i in reactants]

    # sites should be a list of all monomer_binding sites pairs, other
    # than those involved in the binding reaction.
    # Since participating monomers may be identical,(for example in
    # the case of homodimer formation, the monomers are idenitified
    # simply by numbers.
    sites = []

    for i, r in enumerate(reactant_names):
        for j in model.monomers[r].sites:
            if j not in [c.lower()
                         for ind, c in enumerate(reactant_names) if ind != i] and j not in exclude:
                sites.append(str(i) + '_' + j)
              
    conds = [None, ANY]

    site_variants = {i: conds for i in sites}

    combinations = [dict(zip(sites, prod))
                    for prod in it.product(*(site_variants[site]
                                           for site in sites))]

    # Copy original rule and specify occupancy of binding
    # sites (None or ANY) that do not pariticpate in the binding reaction
    for c in range(2**len(sites)):
        if c < 2**len(sites) - 1:
            rule_copy = copy.deepcopy(rule)
        elif c == 2**len(sites) - 1:
            rule_copy = rule
        reactants = get_reactants(rule_copy)
        products = get_products(rule_copy)
        name_string = []
        rate_string = []
        for s in sites:
            rxn_ind = int(re.split('\_', s)[0])
            site_name = re.split('\_', s)[1]
            reactants[rxn_ind] = reactants[rxn_ind](
                **{site_name: combinations[c][s]})
            products[rxn_ind] = products[rxn_ind](
                **{site_name: combinations[c][s]})
            name_string.append(site_name + str(combinations[c][s]))
            # if combinations[c][s] is not None:
            rate_string.append(site_name[0] + str(combinations[c][s])[0])
        rule_copy.name = rule_copy.name + '_' + '_'.join(name_string)
        rule_copy.rate_forward.name = rule_copy.rate_forward.name +\
                                      '_' + ''.join(rate_string)
        
        if c != 2**len(sites) - 1:
            # rule_copy.rename(rule_copy.name)
            model.add_component(rule_copy)
            model.parameters.add(rule_copy.rate_forward)

    return model
