# FILE: MembershipTBDriver.py
# CLASS: MembershipTBDriver
# Driver/tester for the MembershipTRLogic and Membership ADTs.
# Wrapped in a class (rather than a loose script) so the
# individual demo steps are reusable methods you can call
# independently, rerun, or extend with new scenarios.
# Every method here is fully parameterized - nothing is
# hardcoded. This file is meant as a reusable template.
# Tester: Julian V. Bascao

from MembershipTRLogic import MembershipTRLogic


# START OF CLASS: MembershipTBDriver
class MembershipTBDriver:

    # START OF METHOD: __init__ (Constructor / Creator)
    def __init__(self):
        # Each driver instance gets its own fresh tracker, so running
        # the demo twice in the same session never mixes old data
        # into the new run.

        # Attributes (encapsulated / private, underscore prefix)
        self.tracker = MembershipTRLogic()   # identity: the ADT this driver is testing
    # END OF METHOD: __init__

    # START OF METHOD: demo_registration
    def demo_registration(self, name1, contact1, name2, contact2):
        # Registers two members using whatever names/contacts the
        # caller provides, then shows the tracker right after
        # creation, before any activity has happened yet.
        member1 = self.tracker.register_member(name1, contact1)
        member2 = self.tracker.register_member(name2, contact2)

        print("=== After Registration ===")
        print(self.tracker.view_all_members())

        return member1, member2
    # END OF METHOD: demo_registration

    # START OF METHOD: demo_visits
    def demo_visits(self, member, visit_count):
        # Records a chosen number of visits for one member, then
        # shows the badge that unlocked as a result.
        for i in range(visit_count):
            member.record_visit()

        print(f"=== After {member.get_name()}'s {visit_count} Visits ===")
        print(f"{member.get_name()}'s badge: {member.get_badge()}")
        print()
    # END OF METHOD: demo_visits

    # START OF METHOD: demo_renewals
    def demo_renewals(self, member, renewal_count):
        # Renews one member's membership a chosen number of times,
        # then shows the resulting badge and validity.
        for i in range(renewal_count):
            self.tracker.renew_membership(member.get_member_id())

        print(f"=== After {member.get_name()}'s {renewal_count} Renewals ===")
        print(f"{member.get_name()}'s badge: {member.get_badge()}")
        print(f"{member.get_name()} valid? {self.tracker.is_valid_member(member.get_member_id())}")
        print()
    # END OF METHOD: demo_renewals

    # START OF METHOD: demo_unknown_member
    def demo_unknown_member(self, fake_id):
        # Confirms the tracker fails gracefully (returns False) for
        # an ID that was never registered, instead of crashing.
        print("=== Checking a nonexistent member ===")
        print(f"Unknown valid? {self.tracker.is_valid_member(fake_id)}")
        print()
    # END OF METHOD: demo_unknown_member

    # START OF METHOD: demo_deactivate_and_remove
    def demo_deactivate_and_remove(self, member):
        # Manually deactivates a member, confirms they're now
        # invalid, then removes them from the tracker entirely.
        member.deactivate()
        print(f"=== After Deactivating {member.get_name()} ===")
        print(f"{member.get_name()} valid? {self.tracker.is_valid_member(member.get_member_id())}")
        print()

        self.tracker.remove_member(member.get_member_id())
        print(f"=== After Removing {member.get_name()} ===")
        print(f"Total members: {self.tracker.get_total_members()}")
        print(self.tracker.view_all_members())
    # END OF METHOD: demo_deactivate_and_remove

    # START OF METHOD: run
    def run(self, name1, contact1, name2, contact2, visit_count, renewal_count, fake_id):
        # Runs the full demo sequence, end to end, using the smaller
        # demo_* methods above. Every value used here is passed in by
        # the caller - nothing is decided inside this method.
        member1, member2 = self.demo_registration(name1, contact1, name2, contact2)
        self.demo_visits(member1, visit_count)
        self.demo_renewals(member1, renewal_count)
        self.demo_unknown_member(fake_id)
        self.demo_deactivate_and_remove(member2)
    # END OF METHOD: run

# END OF CLASS: MembershipTBDriver

if __name__ == "__main__":
    driver = MembershipTBDriver()