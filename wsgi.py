import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, get_all_admins, get_all_admins_json,
     add_admin, add_alumni, add_company, add_listing, add_categories, remove_categories,
     get_all_companies, get_all_companies_json,
     get_all_alumni, get_all_alumni_json, get_all_listings, get_all_listings_json, get_company_listings, get_all_subscribed_alumni,
     subscribe_action, is_alumni_subscribed, send_notification, apply_listing, get_all_applicants,
     get_user_by_username, get_user,
     login)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')

    # add in the first admin
    add_admin('bob', 'bobpass', 'bob@mail')

    # add in alumni
    add_alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')

    # add_alumni('rooooob', 'robpass', 'roooooob@mail', '123456089')

    add_categories('123456789', ['Database'])
    # print('test')

    # remove_categories('123456789', ['N/A'])
    # remove_categories('123456789', ['Database'])
    

    # subscribe rob
    subscribe_action('123456789')

    # add in companies
    add_company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
    add_company('company2', 'company2', 'compass', 'company@mail2',  'company_address2', 'contact2', 'company_website2.com')

    # add in listings
    # listing1 = add_listing('listing1', 'job description', 'company2')
    # print(listing1, 'test')
    add_listing('listing1', 'job description1', 'company1',
                8000, 'Part-time', True, 'employmentTerm!', True, 'desiredCandidate?', 'Curepe', ['Database', 'Programming', 'butt'])

    add_listing('listing2', 'job description', 'company2',
                4000, 'Full-time', True, 'employmentTerm?', True, 'desiredCandidate?', 'Curepe', ['Database', 'Programming', 'butt'])

    


    # print(get_all_listings_json())
    print(get_company_listings('company2'))
    

    # print(get_all_subscribed_alumni())
    # send_notification(['Programming'])
    # create_user('username', 'password', 'email')
    # print(get_user_by_username('rob'))
    # print(jwt_authenticate('bob', 'bobpass'))

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)