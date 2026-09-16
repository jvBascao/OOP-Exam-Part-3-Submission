# FILE: MembershipMenu.py
# CLASS: MembershipMenu
# Console menu (CLI) for interacting with the MembershipTRLogic
# ADT. Automatically loads existing data from a text file on
# startup, and provides a menu option to save on demand.
# Author: Julian V. Bascao

from MembershipTRLogic import MembershipTRLogic


# START OF CLASS: MembershipMenu
class MembershipMenu:

    # START OF METHOD: __init__ (Constructor / Creator)
    def __init__(self, filename="members.txt"):
        # filename: the text file this menu auto-loads from and
        # saves to (defaults to "members.txt" in the same folder)

        # Attributes (encapsulated / private, underscore prefix)
        self._tracker = MembershipTRLogic()   # identity: the ADT this menu operates on
        self._filename = filename             # identity: where data is loaded from / saved to

        # Try to auto-load existing data. If the file doesn't exist
        # yet (e.g. first time running this program), that's not an
        # error - just start with an empty tracker instead.
        try:
            self._tracker.load_from_file(self._filename)
            print(f"Loaded existing data from '{self._filename}'.")
        except FileNotFoundError:
            print(f"No existing data file found. Starting fresh.")
    # END OF METHOD: __init__

    # START OF METHOD: show_menu
    def show_menu(self):
        # Displays the numbered menu options.
        print("\n[---- MemTrack Menu ----]")
        print("1. Register New Member")
        print("2. Renew Membership")
        print("3. Record a Visit")
        print("4. Check Member Validity")
        print("5. View Member Info")
        print("6. View All Members")
        print("7. Remove Member")
        print("8. Save to File")
        print("9. Exit")
    # END OF METHOD: show_menu

    # START OF METHOD: handle_register
    def handle_register(self):
        name = input("Enter member name: ")
        contact_info = input("Enter contact info (phone/email): ")
        new_member = self._tracker.register_member(name, contact_info)
        print(f"Registered! New member ID: {new_member.get_member_id()}")
    # END OF METHOD: handle_register

    # START OF METHOD: handle_renew
    def handle_renew(self):
        member_id = input("Enter member ID to renew: ")
        success = self._tracker.renew_membership(member_id)
        if success:
            print("Membership renewed successfully.")
        else:
            print("This ID number doesn't exist.")
    # END OF METHOD: handle_renew

    # START OF METHOD: handle_record_visit
    def handle_record_visit(self):
        member_id = input("Enter member ID: ")
        member = self._tracker.find_member(member_id)
        if member is None:
            print("This ID number doesn't exist.")
        else:
            member.record_visit()
            print(f"Visit recorded. {member.get_name()} now has {member.get_visit_count()} visits.")
    # END OF METHOD: handle_record_visit

    # START OF METHOD: handle_check_validity
    def handle_check_validity(self):
        member_id = input("Enter member ID: ")
        member = self._tracker.find_member(member_id)
        if member is None:
            print("This ID number doesn't exist.")
        else:
            print(f"Valid: {member.is_valid()}")
    # END OF METHOD: handle_check_validity

    # START OF METHOD: handle_view_member
    def handle_view_member(self):
        member_id = input("Enter member ID: ")
        member = self._tracker.find_member(member_id)
        if member is None:
            print("This ID number doesn't exist.")
        else:
            print(member.view_info())
    # END OF METHOD: handle_view_member

    # START OF METHOD: handle_view_all
    def handle_view_all(self):
        print(self._tracker.view_all_members())
    # END OF METHOD: handle_view_all

    # START OF METHOD: handle_remove
    def handle_remove(self):
        member_id = input("Enter member ID to remove: ")
        success = self._tracker.remove_member(member_id)
        if success:
            print("Member removed.")
        else:
            print("This ID number doesn't exist.")
    # END OF METHOD: handle_remove

    # START OF METHOD: handle_save
    def handle_save(self):
        self._tracker.save_to_file(self._filename)
        print(f"Saved to '{self._filename}'.")
    # END OF METHOD: handle_save

    # START OF METHOD: run
    def run(self):
        # Main loop: keeps showing the menu and handling choices
        # until the user picks Exit.

        # Simplified staff login placeholder - just asks for a name,
        # no real authentication yet. This exists so the flow
        # matches the approved User Journey ("Log in as staff").
        # TODO: replace with real staff authentication later.
        staff_name = input("Staff login - enter your name: ")
        print(f"Welcome, {staff_name}!")

        running = True
        while running:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.handle_register()
            elif choice == "2":
                self.handle_renew()
            elif choice == "3":
                self.handle_record_visit()
            elif choice == "4":
                self.handle_check_validity()
            elif choice == "5":
                self.handle_view_member()
            elif choice == "6":
                self.handle_view_all()
            elif choice == "7":
                self.handle_remove()
            elif choice == "8":
                self.handle_save()
            elif choice == "9":
                print(f"Goodbye, {staff_name}! Logging out.")
                running = False
            else:
                print("Invalid choice. Please try again.")
    # END OF METHOD: run

# END OF CLASS: MembershipMenu


# START OF MAIN
if __name__ == "__main__":
    menu = MembershipMenu()
    menu.run()
# END OF MAIN