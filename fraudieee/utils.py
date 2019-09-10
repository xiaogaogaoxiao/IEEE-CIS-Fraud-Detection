def find_and_replace(df, column, regex_sentence, replace_value,
                     case=False, inplace=True):
    if inplace:
        df_new = df
    else:
        df_new = df.copy()
    df_new.loc[
        df_new[column].str.contains(regex_sentence, case=case, na=False),
        column
    ] = replace_value

    return df_new if not inplace else None
