class FilterModule(object):

    def filters(self):
        return {
            "parse_nested_members": self.parse_nested_members,
        }

    @staticmethod
    def parse_nested_members(groups: dict, max_nesting_depth: int = 10) -> dict:
        for _ in range(max_nesting_depth):
            # recursion the extension of the members to process nested groups

            for g in groups.values():
                member_key = None
                parent_key = None

                if 'member_of' in g:
                    member_key = 'member_of'

                elif 'parents' in g:
                    member_key = 'parents'

                if 'children' in g:
                    parent_key = 'children'

                elif 'nested_groups' in g:
                    parent_key = 'nested_groups'

                if member_key is not None:
                    for p in g[member_key]:
                        groups[p]['members'].extend(g['members'])

                if parent_key is not None:
                    for c in g[parent_key]:
                        g['members'].extend(groups[c]['members'])

        # removing duplicate members
        for g in groups.values():
            g['members'] = list(set(g['members']))

        return groups
