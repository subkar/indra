from pysb import ANY, Parameter
import pysb
import re
import itertools as it
import copy


def get_reactants(rule):
   reactants = [mp.monomer for
                cp in rule.reactant_pattern.complex_patterns
                for mp in cp.monomer_patterns]
   return reactants


def get_monomer_pattern(rp):
   rpm = [mp for
                cp in rp.complex_patterns
                for mp in cp.monomer_patterns]
   return rpm
   

def enumerate_rules(model, rule, exclude=[]):
    ''' Given a rule, generate rules for all possible combinations, 
    taking into account the binding sites and occupancy for each
    participating monomer in the rule. '''
    
    reactants = get_reactants(rule)
    
    # sites should be a list of all monomer_binding sites pairs, other
    # than those involved in the binding reaction.
    # Since participating monomers may be identical,(for example in
    # the case of homodimer formation, the monomers are idenitified
    # simply by numbers.
    rule_sites = []

    for i, r in enumerate(reactants):
        reactant_sites = []
        for j in r.sites:
            if j not in [c.name.lower()
                         for ind, c in enumerate(reactants) if ind != i] and j not in exclude:
               reactant_sites.append('%s' % j)
        rule_sites.append(reactant_sites)       
              
    conds = [None, ANY]

    # Replace with list of dicts

    site_variants = []    
    for reactant_sites in rule_sites:
        site_variants.append({site: conds for site in reactant_sites})


    combos = []
    for prod in it.product(*(site_variants[ind][site] for ind, reactant_sites in enumerate(rule_sites) for site in reactant_sites)):
        combos.append(prod)

        
    list = []    
    for combo in combos:
        l = get_site_combs(combo, rule_sites)
        if sorted(l) not in [sorted(l2) for l2 in list]:
            list.append(l)


    for c in range(len(list)):
        if c < len(list) - 1:
            rp = pysb.ReactionPattern([])
            # had to use cp.copy() as compared to cp()
            rp.complex_patterns = [cp.copy() for cp in
                                   rule.reactant_pattern.complex_patterns]
            pp = pysb.ReactionPattern([cp.copy() for cp
                                       in rule.product_pattern.complex_patterns])

            rpm = get_monomer_pattern(rp)
            ppm = get_monomer_pattern(pp)

            rate_string = []
            name_string = []
            for i, reactions_sites in enumerate(rule_sites):
                for site in reactions_sites:
                   rpm[i].site_conditions.update({site: list[c][i][site]})
                   ppm[i].site_conditions.update({site: list[c][i][site]})
                    
                   rate_string.append(site[0] + str(list[c][i][site])[0])
                   name_string.append(site + str(list[c][i][site])[0])
            rule_name = '%s_' % rule.name + '_'.join(name_string)
            param_name = '%s_' % rule.rate_forward.name + '_'.join(rate_string)
            new_param = pysb.Parameter(param_name, rule.rate_forward.value)

            new_rule = pysb.Rule(rule_name, rp >> pp, new_param)

            model.add_component(new_rule)
            model.parameters.add(new_param)
        elif c == len(list) -1:
           rpm = get_monomer_pattern(rule.reactant_pattern)
           ppm = get_monomer_pattern(rule.product_pattern)

           rate_string = []
           name_string = []
           for i, reactions_sites in enumerate(rule_sites):
               for site in reactions_sites:
                  rpm[i].site_conditions.update({site: list[c][i][site]})
                  ppm[i].site_conditions.update({site: list[c][i][site]})
                   
                  rate_string.append(site[0] + str(list[c][i][site])[0])
                  name_string.append(site + str(list[c][i][site])[0])
           rule.name = '%s_' % rule.name + '_'.join(name_string)
           rule.rate_forward.name = '%s_' % rule.rate_forward.name + '_'.join(rate_string)
            
    return model


def get_site_combs(comb, rule_sites):
    h = []          
    st = 0
    en = 0

    for reactant_sites in rule_sites:
        en = st + len(reactant_sites)
        pr = comb[st: en]
        # print 'pr: %s' % pr
        d = dict(zip(reactant_sites, pr))
        h.append(d.copy())
        st += len(reactant_sites)
    return h      



    # # Copy original rule and specify occupancy of binding
    # # sites (None or ANY) that do not pariticpate in the binding reaction
    # # 
    # for c in range(2**len(sites)):
    #     if c < 2**len(sites) - 1:
    #         rule_copy = copy.deepcopy(rule)
    #     elif c == 2**len(sites) - 1:
    #         rule_copy = rule
    #     reactants = get_reactants(rule_copy)
    #     products = get_products(rule_copy)
    #     name_string = []
    #     rate_string = []
    #     for s in sites:
    #         rxn_ind = int(re.split('\_', s)[0])
    #         site_name = re.split('\_', s)[1]
    #         reactants[rxn_ind] = reactants[rxn_ind](
    #             **{site_name: combinations[c][s]})
    #         products[rxn_ind] = products[rxn_ind](
    #             **{site_name: combinations[c][s]})
    #         name_string.append(site_name + str(combinations[c][s]))
    #         # if combinations[c][s] is not None:
    #         rate_string.append(site_name[0] + str(combinations[c][s])[0])
    #     rule_copy.name = rule_copy.name + '_' + '_'.join(name_string)
    #     rule_copy.rate_forward.name = rule_copy.rate_forward.name +\
    #                                   '_' + ''.join(rate_string)
        
    #     if c != 2**len(sites) - 1:
    #         # rule_copy.rename(rule_copy.name)
    #         model.add_component(rule_copy)
    #         model.parameters.add(rule_copy.rate_forward)

    # return model




