

#   |￣￣￣￣￣￣￣ |
#   |   START    |
#   |    HERE    |
#   |     ON     |
#   |   MONDAY   |
#   |＿＿＿＿＿＿＿ |
# (\___/) ||
# (• ㅅ •) ||
# / 　   づ

#         /￣￣￣￣￣￣￣/
#        /   START   /
#       /    HERE   /
#      /    ON     /
#     /   MONDAY  /
#    /＿＿＿＿＿＿＿/
# (\_/)  //
# (•ㅅ•) //
# /　 づ


def merge_dictionaries(*argv):
    """
    Merges dictionaries, in the order provided,
     without over-writing keys missing or values of None or ZLS
    precedence goes to key value pairs in latter dicts.
    :rtype: dictionary
    :param argv:
    :return:
    """

    # TODO(JamesBalcomb): add check for key collisions
    # TODO(JamesBalcomb): add argument for specifying logic for handling key collisions

    dictionary_count = len(argv)

    merged_dictionary = argv[0].copy()

    for itr in range(1, dictionary_count):
        for key_name, key_value in argv[itr].items():
            if key_name not in merged_dictionary:
                merged_dictionary[key_name] = key_value
            if merged_dictionary[key_name] is None:
                merged_dictionary[key_name] = key_value
            if merged_dictionary[key_name] == '':
                merged_dictionary[key_name] = key_value

    return merged_dictionary
