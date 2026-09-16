# FILE: MembershipTRLogic.py
# CLASS: MembershipTRLogic
# MembershipTRLogic ADT - manages a collection of Membership
# records. It is the only class that knows about the whole list
# of members, and is responsible for registering, finding,
# renewing, and removing them. Keeping this logic separate from
# Membership itself means Membership stays a simple, reusable
# record class that knows nothing about "the whole list."
# Author: Julian V. Bascao

from Membership import Membership
import datetime


# START OF CLASS: MembershipTRLogic
class MembershipTRLogic:

    # START OF METHOD: __init__ (Constructor / Creator)
    def __init__(self):
        # Creates a tracker with no members yet registered.

        # Attributes (encapsulated / private, underscore prefix)
        self._members = []     # identity: the list holding every registered Membership object
        self._next_id = 1      # identity: counter used to generate the next unique member ID
    # END OF METHOD: __init__

    # START OF SECTION: Observers (read-only, do not change state)

    # START OF METHOD: find_member
    def find_member(self, member_id):
        # Searches for a member by their ID.
        # Returns the matching Membership object, or None if not found.
        for m in self._members:
            if m.get_member_id() == member_id:
                return m
        return None
    # END OF METHOD: find_member

    # START OF METHOD: is_valid_member
    def is_valid_member(self, member_id):
        # Checks whether a specific member exists AND is currently
        # valid. Returns False for a nonexistent ID rather than
        # raising an error, since this is a yes/no question staff
        # will ask constantly - it shouldn't crash the program just
        # because of a typo'd ID.
        m = self.find_member(member_id)
        if m is None:
            return False
        return m.is_valid()
    # END OF METHOD: is_valid_member

    # START OF METHOD: get_total_members
    def get_total_members(self):
        # Returns the total number of members currently tracked.
        return len(self._members)
    # END OF METHOD: get_total_members

    # END OF SECTION: Observers

    # START OF SECTION: Transformers (change internal state)

    # START OF METHOD: register_member
    def register_member(self, name, contact_info):
        # Registers a new member, automatically assigning them a
        # unique zero-padded ID (e.g. "001", "002") so the caller
        # never has to invent one manually.
        # Returns the newly created Membership object.
        member_id = f"{self._next_id:03d}"     # zero-pad to 3 digits, e.g. 1 -> "001"
        self._next_id += 1                     # advance the counter for the NEXT registration
        new_member = Membership(member_id, name, contact_info)  # create the actual object
        self._members.append(new_member)       # store it in the tracked list
        return new_member
    # END OF METHOD: register_member

    # START OF METHOD: renew_membership
    def renew_membership(self, member_id):
        # Renews a member's expiry date by one year, if they exist.
        # Returns True if the member was found and renewed, False
        # otherwise - lets the caller decide how to react instead of
        # this method deciding for them.
        m = self.find_member(member_id)
        if m is None:
            return False
        m.renew()
        return True
    # END OF METHOD: renew_membership

    # START OF METHOD: remove_member
    def remove_member(self, member_id):
        # Removes a member's record entirely from the tracker.
        # Returns True if a matching member was found and removed.
        m = self.find_member(member_id)
        if m is None:
            return False
        self._members.remove(m)
        return True
    # END OF METHOD: remove_member

    # END OF SECTION: Transformers

    # START OF SECTION: Input/Output

    # START OF METHOD: view_all_members
    def view_all_members(self):
        # Lists every currently tracked member's summary info, useful
        # for a staff-facing overview screen.
        if not self._members:
            return "No members registered yet."
        result = ""
        for m in self._members:
            result += m.view_info() + "\n---\n"
        return result
    # END OF METHOD: view_all_members

    # START OF METHOD: save_to_file
    def save_to_file(self, filename):
        # Writes every tracked member to a text file, one member per
        # line, fields separated by "|". Explicitly uses UTF-8
        # encoding so names/contact info with special characters
        # (accents, non-English letters, etc.) are stored correctly.
        with open(filename, "w", encoding="utf-8") as file:
            for m in self._members:
                line = (
                    f"{m.get_member_id()}|{m.get_name()}|{m.get_contact_info()}|"
                    f"{m.get_join_date()}|{m.get_expiry_date()}|"
                    f"{m.is_marked_active()}|{m.get_visit_count()}|{m.get_renewal_count()}\n"
                )
                file.write(line)
    # END OF METHOD: save_to_file

    # START OF METHOD: load_from_file
    def load_from_file(self, filename):
        # Reads a previously saved file and rebuilds the member list
        # from it, replacing whatever was in memory. Also explicitly
        # reads using UTF-8, matching how it was written, so nothing
        # gets misread or corrupted going back the other way.
        self._members = []
        highest_number_seen = 0

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue

                parts = line.split("|")
                member_id = parts[0]
                name = parts[1]
                contact_info = parts[2]
                join_date = datetime.date.fromisoformat(parts[3])
                expiry_date = datetime.date.fromisoformat(parts[4])
                active = (parts[5] == "True")
                visit_count = int(parts[6])
                renewal_count = int(parts[7])

                restored_member = Membership(
                    member_id, name, contact_info,
                    join_date, expiry_date, active,
                    visit_count, renewal_count
                )
                self._members.append(restored_member)

                # keep track of the highest ID number seen, so new
                # registrations after loading don't accidentally
                # reuse an ID that already exists
                number_part = int(member_id)
                if number_part > highest_number_seen:
                    highest_number_seen = number_part

        self._next_id = highest_number_seen + 1
    # END OF METHOD: load_from_file

    # END OF SECTION: Input/Output

# END OF CLASS: MembershipTRLogic