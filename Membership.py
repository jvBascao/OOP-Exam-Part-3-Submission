# FILE: Membership.py
# CLASS: Membership
# Membership ADT - represents a single individual's membership
# record, including its validity period and engagement activity
# (visits and renewals), used to award simple recognition badges.
# Author: Julian V. Bascao

# User Journey:
# 1. Open the application and initialize the core system architecture.
# 2. Log in as a staff member using secure credentials and establish a user session.
# 3. Search for an existing member record, or register a new member profile if they do not yet have an account.
# 4. View the member's comprehensive account details and current status (active or expired).
# 5. Process membership renewals if the account has expired or is expiring soon.
# 6. Record daily check-ins to track member visits and drive automated engagement metrics.
# 7. Evaluate and update loyalty points, tracking total renewals to reward long-term commitment.
# 8. Award automated recognition badges (New Member, Regular, Loyal Member, Returning Member, Veteran Member) 
# - based on accumulated visits and renewals.
# 9. Confirm, validate, and persist the updated member records to the database.
# 10. Log out securely and terminate the active staff session.

import datetime


# START OF CLASS: Membership
class Membership:

    # START OF METHOD: __init__ (Constructor / Creator)
    def __init__(self, member_id, name, contact_info,
                 join_date=None, expiry_date=None, active=True,
                 visit_count=0, renewal_count=0):
        # Creates a Membership. Called two different ways:
        #   1. New member: only member_id/name/contact_info given -
        #      the rest default to "brand new" values.
        #   2. Restored member (loaded from a file): every value is
        #      passed in explicitly, recreating an existing record
        #      exactly as it was saved.
        # member_id: a unique identifier for this member
        # name: the member's name
        # contact_info: phone number or email

        # Attributes (encapsulated / private, underscore prefix)
        self._member_id = member_id            # identity: unique ID string, e.g. "M1"
        self._name = name                      # identity: the member's full name
        self._contact_info = contact_info      # identity: phone number or email
        self._join_date = join_date if join_date is not None else datetime.date.today()
        self._expiry_date = expiry_date if expiry_date is not None else (datetime.date.today() + datetime.timedelta(days=365))
        self._active = active                  # identity: manually controlled on/off switch, separate from expiry
        self._visit_count = visit_count        # identity: how many times record_visit() has been called
        self._renewal_count = renewal_count    # identity: how many times renew() has been called
    # END OF METHOD: __init__

    # START OF SECTION: Observers (read-only, do not change state)

    def get_member_id(self):
        return self._member_id

    def get_name(self):
        return self._name

    def get_contact_info(self):
        return self._contact_info

    def get_join_date(self):
        return self._join_date

    def get_expiry_date(self):
        return self._expiry_date

    def get_visit_count(self):
        return self._visit_count

    def get_renewal_count(self):
        return self._renewal_count

    # START OF METHOD: is_marked_active
    def is_marked_active(self):
        # Returns the raw active flag on its own, separate from
        # is_valid() (which also checks the expiry date). Needed so
        # saving to a file stores the EXACT state, not a derived one.
        return self._active
    # END OF METHOD: is_marked_active

    # START OF METHOD: is_valid
    def is_valid(self):
        # A member is valid only if they are marked active AND their
        # expiry date has not yet passed.
        return self._active and datetime.date.today() <= self._expiry_date
    # END OF METHOD: is_valid

    # START OF METHOD: get_badge
    def get_badge(self):
        # Determines this member's recognition badge based on their
        # renewal count and visit count. Renewal loyalty is checked
        # first (it reflects long-term tenure); visit frequency is
        # checked next, so active new members are still recognized.
        if self._renewal_count >= 5:
            return "Veteran Member"
        elif self._renewal_count >= 2:
            return "Returning Member"
        elif self._visit_count >= 20:
            return "Loyal Member"
        elif self._visit_count >= 5:
            return "Regular"
        else:
            return "New Member"
    # END OF METHOD: get_badge

    # END OF SECTION: Observers

    # START OF SECTION: Transformers (change internal state)

    # START OF METHOD: renew
    def renew(self):
        # Extends this member's expiry date by one year from today
        # and reactivates the membership, then records the renewal.
        self._expiry_date = datetime.date.today() + datetime.timedelta(days=365)
        self._active = True
        self._renewal_count += 1
    # END OF METHOD: renew

    # START OF METHOD: record_visit
    def record_visit(self):
        # Records a single visit/check-in for this member, used to
        # build up their visit-based badge eligibility over time.
        self._visit_count += 1
    # END OF METHOD: record_visit

    # START OF METHOD: deactivate
    def deactivate(self):
        # Manually deactivates this membership (e.g., cancelled by
        # the member, or suspended by staff), separate from natural
        # expiry.
        self._active = False
    # END OF METHOD: deactivate

    # END OF SECTION: Transformers

    # START OF SECTION: Input/Output

    # START OF METHOD: view_info
    def view_info(self):
        # Returns a human-readable summary of this member's current record.
        return (
            f"ID: {self._member_id}\n"
            f"Name: {self._name}\n"
            f"Contact: {self._contact_info}\n"
            f"Joined: {self._join_date}\n"
            f"Expires: {self._expiry_date}\n"
            f"Valid: {self.is_valid()}\n"
            f"Visits: {self._visit_count}\n"
            f"Renewals: {self._renewal_count}\n"
            f"Badge: {self.get_badge()}"
        )
    # END OF METHOD: view_info

    # END OF SECTION: Input/Output

# END OF CLASS: Membership