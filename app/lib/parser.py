import sys
import pprint

import defusedxml.minidom as minidom # Use defusedxml instead of python built-in, as the built-in is vulnerable to DoS attacks.

TAG_MAP = {
    'ein'              : ('EIN', 'RecipientEIN', 'EINOfRecipient'),
    'address'          : ('USAddress', 'AddressUS'),
    'business_name'    : ('Name', 'RecipientNameBusiness', 'BusinessName', 'RecipientBusinessName'),
    'business_name_txt': ('BusinessNameLine1', 'BusinessNameLine1Txt'),
    'address_line_txt' : ('AddressLine1', 'AddressLine1Txt'),
    'city'             : ('City', 'CityNm'),
    'state'            : ('State', 'StateAbbreviationCd'),
    'zip'              : ('ZIPCode', 'ZIPCd'),
    'amount'           : ('AmountOfCashGrant', 'CashGrantAmt'),
    'purpose'          : ('PurposeOfGrant', 'PurposeOfGrantTxt'),
    'irc'              : ('IRCSection'),
   } 

def get_text( nodes ):
    text_list = []
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            text_list.append(node.data)
    return ''.join(text_list)


def parse_entity_info( entity ):
    # EINs can be missing
    ein = None
    for ein_key in TAG_MAP['ein']:
        ein_elems = entity.getElementsByTagName( ein_key )
        if len(ein_elems) > 0:
            ein_elem = ein_elems[0]
            ein = get_text( ein_elem.childNodes )
            break
    results = {'ein': ein}

    # TODO: Review xml schema for AddressLine2 etc.
    address = {}
    for address_key in TAG_MAP['address']:
        address_elems = entity.getElementsByTagName( address_key )
        if len(address_elems) > 0:
            address_elem = address_elems[0]
            for tag_list in ('address_line_txt', 'city', 'state', 'zip',):
                for tag in TAG_MAP[tag_list]:
                    elems = address_elem.getElementsByTagName( tag )
                    if len(elems) > 0:
                        elem = elems[0]
                        address[tag_list] = get_text( elem.childNodes )
    results['address'] = address
        
    # TODO: Review xml schema for BusinessNameLine2 etc.
    business_name = None
    for business_key in TAG_MAP['business_name']:
        business_elems = entity.getElementsByTagName( business_key )
        if len(business_elems) > 0:
            business_elem = business_elems[0]
            for tag in TAG_MAP['business_name_txt']:
                elems = business_elem.getElementsByTagName( tag )
                if len(elems) > 0:
                    business_name = get_text( elems[0].childNodes )
    results['business_name'] = business_name
    return results


def parse_grant_info( entity ):
    results = {}
    for tag_list in ('amount', 'purpose', 'irc'):
        for tag in TAG_MAP[tag_list]:
            elems = entity.getElementsByTagName(tag)
            if len(elems) > 0:
                results[tag_list] = get_text( elems[0].childNodes )
    return results


def parse( text ):
    # Format described here: https://docs.opendata.aws/irs-990/readme.html
    dom = minidom.parseString(text)
        
    filers = []
    return_elems = dom.getElementsByTagName('Return')
    for return_elem in return_elems:
        return_header_elems = return_elem.getElementsByTagName('ReturnHeader')
        for return_header_elem in return_header_elems:
            filer_elems = return_header_elem.getElementsByTagName('Filer')
            for filer_elem in filer_elems:
                filers.append(filer_elem)

    # Sanity check
    if len(filers) != 1:
        print(f'ERROR filer count: {len(filers)}')
        return None
        
    filer = filers[0]

    results = {}
    entity_data = parse_entity_info( filer )
    results['filer'] = entity_data
    
    awards = []
    for return_elem in return_elems:
        return_data_elems = return_elem.getElementsByTagName('ReturnData')
        for return_data in return_data_elems:
            schedule_i_elems = return_data.getElementsByTagName('IRS990ScheduleI')
            for schedule_i_elem in schedule_i_elems:
                recipient_elems = schedule_i_elem.getElementsByTagName('RecipientTable')
                for recipient_elem in recipient_elems:
                    entity_data = parse_entity_info( recipient_elem )
                    grant_data = parse_grant_info( recipient_elem )
                    awards.append( { 'entity': entity_data, 'grant': grant_data } )

    results['awards'] = awards
    return results
