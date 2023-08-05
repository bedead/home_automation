from routes.__config__ import Config

supabase = Config.supabase_


def update_User_Metadata_User_Type(user_id, type):
    # Table name for user data
    """
    this function updates the "user-type" metadata for a
    user in the Supabase database. It retrieves the
    user's existing metadata, adds the new user
    type information, and updates the
    user's row in the database with the updated metadata.
    """
    table_name = "auth.users"

    # Find the user row based on the user_id
    user_row = (
        supabase.table(table_name).select().eq("id", user_id).execute().get("data")[0]
    )

    if user_row:
        new_metadata = {
            "user-type": type,
        }
        # Update the user_metadata value
        updated_metadata = {**user_row["user_metadata"], **new_metadata}
        update_data = {"user_metadata": updated_metadata}

        # Update the row with the new user_metadata value
        supabase.table(table_name).update(update_data).eq("id", user_id).execute()
        print("User metadata updated successfully.")
    else:
        print("User not found.")
