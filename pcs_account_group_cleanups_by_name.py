""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'prefix',
    type=str,
    help='The prefix of account group')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the current list of Account Groups ...', end='')
cloud_account_group_list_current = pc_api.cloud_account_group_list_read()
print(' done.')
print()

cloud_account_groups_match_search_count = 0
prefix_length=len(args.prefix)


cloud_account_groups_to_cleanup = []
for cloud_account_group_current in cloud_account_group_list_current:
    if cloud_account_group_current['name'].lower()[0:prefix_length] == args.prefix:
        cloud_account_group = {}
        cloud_account_group['name'] = cloud_account_group_current['name']
        cloud_account_group['id'] = cloud_account_group_current['id']
        cloud_account_group['description'] = cloud_account_group_current['description']
        cloud_account_group['accountIds'] = []
        cloud_account_groups_to_cleanup.append(cloud_account_group)

print('Cloud Account Groups to Cleanup: %s' % len(cloud_account_groups_to_cleanup))

print('API - Creating Cloud Account Groups ...')
for cloud_account_group_to_cleanup in cloud_account_groups_to_cleanup:
    print('Emptying Cloud Account Group: %s' % cloud_account_group_to_cleanup['name'])
    pc_api.cloud_account_group_update(cloud_account_group_to_cleanup['id'],cloud_account_group_to_cleanup)
    print('Removing Cloud Account Group: %s' % cloud_account_group_to_cleanup['name'])
    pc_api.cloud_account_group_delete(cloud_account_group_to_cleanup['id'])
print()
print('Clean up completed')

