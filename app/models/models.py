from collections import defaultdict

import app.lib.db as db

def write_entity( entity ):
    # TODO: Some entities are missing EINs.
    lookup_entity_sql = 'SELECT entity_id FROM entities where ein = %s'
    insert_entity_sql = '''INSERT INTO entities (name, ein, address_line_1, city, state, zip) 
                           VALUES (%s, %s, %s, %s, %s, %s)'''
    address = entity['address']
    with db.ctx_db_cursor() as cursor:
        cursor.execute( lookup_entity_sql, (entity['ein'],) )
        rs = cursor.fetchall()
        for row in rs:
            entity['entity_id'] = row[0]
            return entity
        cursor.execute( insert_entity_sql, (entity['business_name'], entity['ein'], address['address_line_txt'], address['city'], address['state'], address['zip'],))
        entity['entity_id'] = cursor.lastrowid
    return entity


def write_filing( data, filer ):
    insert_filing_sql = 'INSERT INTO filings (entity_id, irs_form_id) VALUES (%s, %s)'
    with db.ctx_db_cursor() as cursor:
        cursor.execute( insert_filing_sql, (filer['entity_id'], data['form_id'], ))
        data['filing_id'] = cursor.lastrowid
    return data['filing_id']


def write_award(filing_id, awardee, grant):
    insert_award_sql = '''INSERT INTO awards (filing_id, recipient_entity_id, amount, purpose, irc_section) 
                          VALUES (%s, %s, %s, %s, %s)'''
    with db.ctx_db_cursor() as cursor:
        cursor.execute( insert_award_sql, (filing_id, awardee['entity_id'], grant['amount'], grant.get('purpose'), grant.get('irc'),))


def write_to_db( data ):
    form_id = data['form_id']
    lookup_filing_sql = 'SELECT filing_id FROM filings WHERE irs_form_id = %s'
    lookup_entity_sql = 'SELECT entity_id FROM entities where ein = %s'

    with db.ctx_db_cursor() as cursor:
        cursor.execute( lookup_filing_sql, (form_id,) )
        rs = cursor.fetchall()
        for row in rs:
            # We've already processed this data, don't do it again.
            return

    filer = write_entity( data['filer'] )
    filing_id = write_filing( data, filer )
    for award in data['awards']:
        awardee = write_entity( award['entity'] )
        write_award( filing_id, awardee, award['grant'] )


def read_receivers( state ):
    lookup_sql = '''SELECT entity_id, name, ein, address_line_1, city, state, zip, SUM(amount) as award_totals FROM entities AS e
                    INNER JOIN awards AS a ON a.recipient_entity_id = e.entity_id WHERE e.state = %s GROUP BY entity_id'''
    receivers = []
    with db.ctx_db_dict_cursor() as cursor:
        cursor.execute( lookup_sql, (state,) )
        rs = cursor.fetchall()
        for row in rs:
            results = dict(row)
            # TODO: Deal with MySQL's wonky aggregate Decimal typing.
            del results['award_totals']
            receivers.append( results )
    return receivers


def read_filings():
    lookup_entities_sql = 'SELECT entity_id, name, ein, address_line_1, city, state, zip FROM entities'
    lookup_awards_sql = 'SELECT award_id, filing_id, recipient_entity_id, amount, purpose, irc_section FROM awards'
    lookup_filings_sql = 'SELECT filing_id, entity_id, irs_form_id FROM filings'

    entities = {}
    awards = defaultdict(list)
    filings = []

    with db.ctx_db_dict_cursor() as cursor:
        cursor.execute( lookup_entities_sql )
        rs = cursor.fetchall()
        for row in rs:
            results = dict(row)
            entities[results['entity_id']] = results
        cursor.execute( lookup_awards_sql )
        rs = cursor.fetchall()
        for row in rs:
            results = dict(row)
            results['recipient_entity'] = entities[results['recipient_entity_id']]
            awards[results['filing_id']].append(results)
        cursor.execute( lookup_filings_sql )
        rs = cursor.fetchall()
        for row in rs:
            results = dict(row)
            results['awards'] = awards[results['filing_id']]
            results['filer'] = entities[results['entity_id']]
            filings.append(results)

    return filings
