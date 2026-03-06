import os
import getpass
from datetime import datetime, time

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False

ADMIN_PASSWORD = "team16"

votes_file = "votes.txt"
voters_file = "voters.txt"
log_file = "log.txt"
report_file = "results_report.txt"
config_file = "election_config.txt"

voting_open = True

candidates = {
    "Pranathi M S": 0,
    "Mehek": 0,
    "Theju": 0,
    "Rahul S Baisani": 0,
    "Swathi": 0,
    "Suchitra S S": 0,
    "Aishwarya": 0,
    "Chaitanya": 0
}

voters = {}
voter_names = set()

election_name = "Default Election"
election_year = "2026"
election_location = "Unknown"

VOTING_START = time(9,0)
VOTING_END = time(23,0)


def write_log(message):
    with open(log_file,"a") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def backup_files():
    if os.path.exists(votes_file):
        with open(votes_file) as src, open("votes_backup.txt","w") as dst:
            dst.write(src.read())

    if os.path.exists(voters_file):
        with open(voters_file) as src, open("voters_backup.txt","w") as dst:
            dst.write(src.read())


def load_config():
    global election_name,election_year,election_location

    if os.path.exists(config_file):
        with open(config_file) as f:
            lines=f.readlines()

            if len(lines)>=3:
                election_name=lines[0].strip()
                election_year=lines[1].strip()
                election_location=lines[2].strip()

    else:
        with open(config_file,"w") as f:
            f.write("Class Representative Election\n2026\nDSATM\n")


def save_vote(voter_id,name,candidate):
    with open(votes_file,"a") as f:
        f.write(f"{voter_id},{name},{candidate},{datetime.now()}\n")


def save_voter(voter_id,name,age,gender):
    with open(voters_file,"a") as f:
        f.write(f"{voter_id},{name},{age},{gender}\n")


def load_previous_data():

    if os.path.exists(voters_file):

        with open(voters_file) as f:

            for line in f:

                voter_id,name,age,gender=line.strip().split(",")

                voters[voter_id]={"name":name,"age":int(age),"gender":gender}

                voter_names.add(name.lower())

    if os.path.exists(votes_file):

        with open(votes_file) as f:

            for line in f:

                voter_id,name,candidate,timestamp=line.strip().split(",",3)

                if candidate in candidates:

                    candidates[candidate]+=1


def show_candidates():

    print("\n----- Candidate List -----")

    for i,c in enumerate(candidates,start=1):

        print(f"{i}. {c}")

    print("Total Candidates:",len(candidates))


def validate_age():

    age=input("Enter Age: ")

    if not age.isdigit():

        print("Age must be number")

        return None

    age=int(age)

    if age<18:

        print("Must be 18+")

        return None

    return age


def validate_gender():

    g=input("Enter Gender (M/F/O): ").lower()

    if g in ["m","male"]:

        return "Male"

    if g in ["f","female"]:

        return "Female"

    if g in ["o","others","other"]:

        return "Others"

    print("Invalid gender")

    return None


def validate_voter_id():

    vid=input("Enter Voter ID (numbers only): ")

    if not vid.isdigit():

        print("Numbers only")

        return None

    if vid in voters:

        print("Already voted")

        return None

    return vid


def voting_time_allowed():

    now=datetime.now().time()

    if now<VOTING_START or now>VOTING_END:

        return False

    return True


def register_and_vote():

    global voting_open

    if not voting_open:

        print("Voting closed by admin")

        return

    if not voting_time_allowed():

        print("Voting allowed only between 9:00 and 23:00")

        return

    print("\n----- Voter Registration -----")

    name=input("Enter Name: ").strip()

    key=name.lower()

    if key in voter_names:

        print("Already voted")

        return

    age=validate_age()

    if age is None: return

    gender=validate_gender()

    if gender is None: return

    vid=validate_voter_id()

    if vid is None: return

    show_candidates()

    c=input("Enter candidate number: ")

    if not c.isdigit():

        print("Invalid")

        return

    c=int(c)

    if c<1 or c>len(candidates):

        print("Out of range")

        return

    candidate=list(candidates.keys())[c-1]

    confirm=input(f"Confirm vote for {candidate}? (Y/N): ").lower()

    if confirm!="y":

        print("Cancelled")

        return

    candidates[candidate]+=1

    voters[vid]={"name":name,"age":age,"gender":gender}

    voter_names.add(key)

    save_vote(vid,name,candidate)

    save_voter(vid,name,age,gender)

    backup_files()

    write_log(f"{name} voted for {candidate}")

    print("Vote recorded")


def admin_login():

    pw=getpass.getpass("Enter Admin Password: ")

    if pw==ADMIN_PASSWORD:

        return True

    print("Wrong password")

    return False


def calculate_results():

    total=sum(candidates.values())

    if total==0:

        print("No votes yet")

        return

    print("\n----- Results -----")

    for c,v in candidates.items():

        percent=(v/total)*100

        print(f"{c} : {v} votes ({percent:.2f}%)")

    winner=max(candidates,key=candidates.get)

    print("Winner:",winner)

    write_log("Admin viewed results")


def export_results():

    total=sum(candidates.values())

    with open(report_file,"w") as f:

        f.write("Election Results\n")

        f.write("----------------\n")

        for c,v in candidates.items():

            percent=(v/total)*100 if total>0 else 0

            f.write(f"{c} : {v} votes ({percent:.2f}%)\n")

        f.write("\nTotal Votes:"+str(total))

    print("Report generated:",report_file)

    write_log("Admin exported results")


def vote_graph():

    if not MATPLOTLIB_AVAILABLE:

        print("Matplotlib not installed")

        return

    names=list(candidates.keys())

    votes=list(candidates.values())

    plt.bar(names,votes)

    plt.xticks(rotation=45)

    plt.title("Election Vote Graph")

    plt.ylabel("Votes")

    plt.show()


def add_candidate():

    name=input("Candidate name: ").title()

    if name in candidates:

        print("Exists")

        return

    candidates[name]=0

    write_log(f"Candidate added {name}")


def remove_candidate():

    name=input("Candidate name to remove: ").title()

    if name in candidates:

        del candidates[name]

        write_log(f"Candidate removed {name}")

    else:

        print("Not found")


def admin_panel():

    global voting_open

    if not admin_login():

        return

    while True:

        print("\n====== ADMIN PANEL ======")

        print("1 Show Results")

        print("2 Candidate Management")

        print("3 Voting Control")

        print("4 View Logs")

        print("5 Export Results")

        print("6 Vote Graph")

        print("7 Back")

        c=input("Choice: ")

        if c=="1":

            calculate_results()

        elif c=="2":

            while True:

                print("\n--- Candidate Management ---")

                print("1 Add Candidate")

                print("2 Remove Candidate")

                print("3 Edit Candidate Name")

                print("4 Show Candidates")

                print("5 Back")

                cc=input("Choice: ")

                if cc=="1":

                    add_candidate()

                elif cc=="2":

                    remove_candidate()

                elif cc=="3":

                    old=input("Candidate name to edit: ").title()

                    if old in candidates:

                        new=input("New name: ").title()

                        candidates[new]=candidates.pop(old)

                        print("Updated")

                    else:

                        print("Not found")

                elif cc=="4":

                    show_candidates()

                elif cc=="5":

                    break

        elif c=="3":

            voting_open=not voting_open

            print("Voting toggled")

        elif c=="4":

            if os.path.exists(log_file):

                print(open(log_file).read())

        elif c=="5":

            export_results()

        elif c=="6":

            vote_graph()

        elif c=="7":

            break


load_config()

load_previous_data()


while True:

    print("\n==============================")

    print("        VOTING SYSTEM")

    print("==============================")

    print("1 Register & Vote")

    print("2 Show Candidates")

    print("3 Admin Panel")

    print("4 Exit")

    ch=input("Enter choice: ")

    if ch=="1":

        register_and_vote()

    elif ch=="2":

        show_candidates()

    elif ch=="3":

        admin_panel()

    elif ch=="4":

        print("Exiting system")

        break

    else:

        print("Invalid choice")
        