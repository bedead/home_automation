from __config__ import Config
supabase = Config.supabase_

def update_User_Metadata_First_Login(user_id, value):
    # Table name for user data
    table_name = 'auth.users'

    # Find the user row based on the user_id
    user_row = supabase.table(table_name).select().eq('id', user_id).execute().get('data')[0]

    if user_row:
        user_type = user_row['user_metadata']['user-type']
        new_metadata = {
                "user-type": user_type,
                "first-login": value,
            }
        
        # Update the user_metadata value
        updated_metadata = {**user_row['user_metadata'], **new_metadata}
        update_data = {'user_metadata': updated_metadata}

        # Update the row with the new user_metadata value
        supabase.table(table_name).update(update_data).eq('id', user_id).execute()
        print('User metadata updated successfully.')
    else:
        print('User not found.')


def update_User_Metadata_User_Type(user_id, type):
    # Table name for user data
    table_name = 'auth.users'

    # Find the user row based on the user_id
    user_row = supabase.table(table_name).select().eq('id', user_id).execute().get('data')[0]

    if user_row:
        new_metadata = {
                "user-type": type,
                "first-login": False,
            }
        # Update the user_metadata value
        updated_metadata = {**user_row['user_metadata'], **new_metadata}
        update_data = {'user_metadata': updated_metadata}

        # Update the row with the new user_metadata value
        supabase.table(table_name).update(update_data).eq('id', user_id).execute()
        print('User metadata updated successfully.')
    else:
        print('User not found.')