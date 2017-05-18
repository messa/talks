
def test_classic_way_with_asserts(testdb):
    campaign_id = insert_fixture_campaign(testdb)
    app = App(testdb)
    response = app.get_campaign(campaign_id)
    assert response['name'] == 'Test campaign'
    assert response['slug'] == 'test-campaign'
    assert response['targeting']['segment'] == 'customers'
    # assert ...


# ----------------------------------------------------------------  
  
  
def test_against_stored_response(testdb):
    campaign_id = insert_fixture_campaign(testdb)
    app = App(testdb)
    response = app.get_campaign(campaign_id)
    with open('output_get_campaign.yaml', 'w') as f:
        f.write(yaml.dump(response))
    assert not git_dirty('output_get_campaign.yaml')
    # to see what has changed:
    # $ git diff output_get_campaign.yaml
    # to mark response as valid:
    # $ git add output_get_campaign.yaml
        
def git_dirty(path):
    status = subprocess.check_output(
        ['git', 'status', '--porcelain', path], 
        universal_newlines=True)
    return len(status) >= 2 and status[1] != ' '


# ----------------------------------------------------------------  


def test_create_campaign_db_snapshot(testdb):
    app = App(testdb)
    app.create_campaign(id=100, name='Test campaign', ...)
    dump_db(testdb, 'db_after_create_campaign.yaml')
    assert not git_dirty('db_after_create_campaign.yaml')
    
    
def test_get_campaign_based_on_db_snapshot(testdb):
    # instead of "expensive" setup we can just recreate the db content
    # from snapshot created in the previous test
    restore_db(testdb, 'db_after_create_campaign.yaml')
    app = App(testdb)
    response = app.get_campaign(100)
    with open('output_get_campaign.yaml', 'w') as f:
        f.write(yaml.dump(response))
    assert not git_dirty('output_get_campaign.yaml')
    
    
'''
Tips:

- yaml.dump(obj, default_flow_style=False, width=120)
- normalize random ids, datetimes etc. before saving

'''