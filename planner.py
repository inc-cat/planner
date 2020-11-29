from datetime import datetime as dt
from pandas import DataFrame as df
from copy import deepcopy as dc
from data import word_strings
from time import sleep
import pickle
import csv

# Anwar Louis made this
# November 2020


class planner:
    def __init__(self):
        # gathers current entries
        pickle_in = open("data/planner.pickle", "rb")
        self.diary = pickle.load(pickle_in)

        # reading past entries
        pickle_in = open("data/past.pickle", "rb")
        self.past = pickle.load(pickle_in)

        # diary key to index
        # 0: start date/ time, 1: end date/ time 2: activity
        # 3: priority 4: quick notes

        # length of diary entry list for use in loops
        diary_len = len(self.diary)
        # empty list to put index numbers of past entries in current
        # these indexes will be moved into past out of the current list
        past_index = []

        # past entry indexes will be put in the above list from this loop
        for find_past in range(diary_len):
            if self.diary[find_past][1] < dt.now():
                past_index.append(find_past)

        # index list is reversed to stop index errors when pop function is used
        past_index.reverse()

        # pop function is used to move past entries from diary to past list
        for past_transfer in past_index:
            new_past = self.diary.pop(past_transfer)
            self.past.append(new_past)

        self.format_strings = ["======"]

        self.column_list = ["Start", "Finish", "Plan", "Priority", "Notes"]

        # test entries
        # self.diary.append([dt(2020, 12, 12, 19, 45),
        #     dt(2020, 12, 30, 23, 0), "Test", "High", "Cake"])
        # self.diary.append([dt(2020, 12, 31, 8, 30),
        #     dt(2020, 12, 31, 23, 34), "NYE", "High", "Jubilee line"])

    def header(self, header_text):
        # will clear screen and format screen to show time
        # header_text gets printed as the header title

        # defining date for header
        header_now = dt.now()
        # formatting of the time for the header
        print(header_now.strftime("\033c%A \n%d/%B/%Y \n%H:%M"))
        # formatting to show header text
        print(self.format_strings[0])
        print(header_text)
        print(self.format_strings[0])

    def clash_find(self, period_1, period_2):
        # defines the length of the diary for the loops below
        diary_length = len(self.diary)
        # clashes are added into each list as a defined value
        # all details are put in here
        clash_list = []
        # "blank string" goes here for dataframe
        clash_index = []
        # the index of the clash in the list is in here
        clash_value = []

        for start_finish in range(diary_length):
            # if the start is between any of the events in the list
            # this will be caught and data will be added to the list
            # and the loop will restart
            if self.diary[start_finish][0] < period_1 < self.diary[start_finish][1]:
                clash_list.append(self.diary[start_finish])
                clash_index.append(" ")
                clash_value.append(start_finish)
                continue
            # if the end is between any of the events on the list
            elif self.diary[start_finish][0] < period_2 < self.diary[start_finish][1]:
                clash_list.append(self.diary[start_finish])
                clash_index.append(" ")
                clash_value.append(start_finish)
                continue
            # if any start in the list is between the new plans
            elif period_1 < self.diary[start_finish][0] < period_2:
                clash_list.append(self.diary[start_finish])
                clash_index.append(" ")
                clash_value.append(start_finish)
                continue
            # if any finish in the list is between the new plans
            elif period_1 < self.diary[start_finish][1] < period_2:
                clash_list.append(self.diary[start_finish])
                clash_index.append(" ")
                clash_value.append(start_finish)
                continue

            else:
                # if none are found, we continue as normal
                pass

        # if there are no clashes found, the cycle will end and return
        # False for no clashes and None for indexes of entries to check/ delete
        if len(clash_list) < 1:
            return([False, None])
        else:
            pass

        # deep copy clash list to prevent cloning
        clash_table = dc(clash_list)

        # abbreviating dates within the table to make it more readable
        for abb in range(len(clash_list)):
            # if the date is the same for start and finish, it will omit
            # it in the finish time column
            if clash_table[abb][0].strftime \
            ("%A %d %B %Y") == clash_table[abb][1].strftime("%A %d %B %Y"):
                new_date = clash_table[abb][1].strftime("%X")
                clash_table[abb][1] = new_date

        # printing clash note
        print(word_strings.strings.clash_note)
        # results are added to a dataframe
        cl_list = df(
            clash_list,
            index=clash_value, columns=self.column_list
            )
        # print dataframe
        print(cl_list)

        # reuturning clash list and clash indexes for possible deletion
        return([True, clash_value])

    def save_new(self, new_save):
        # new_save is the list entry containing the detals of the plan
        self.diary.append(new_save)

        # saves data to pickle file in data folder
        pickle_out = open("data/planner.pickle", "wb")
        pickle.dump(self.diary, pickle_out)
        pickle_out.close()

    def showing_results(self):
        # showing entries in the list in a dataframe for readabolity
        # if there are no entries in the diary, "no entries will be shown"
        if len(self.diary) == 0:
            print("No entries")
            return False
        else:
            # one line loop to make a list of empty strings for dataframe
            # deck_column = ["" for column_deck in range(len(self.diary))]
            deck_column = []
            for dd in range(len(self.diary)):
                deck_column.append(dd)

            # another deep copy for diary
            current_diary = dc(self.diary)

            # this is to abbreviate dates that are the same for readability
            for abb in range(len(current_diary)):
                if current_diary[abb][0].strftime("%A %d %B %Y") == current_diary[abb][1].strftime("%A %d %B %Y"):
                    new_date = current_diary[abb][1].strftime("%X")
                    current_diary[abb][1] = new_date

            # showing all as a dataframe
            show_all = df(
                current_diary,
                index=deck_column,
                columns=self.column_list
                )

            # print dataframe
            print(show_all)
            # true
            return True

    def return_type(self):
        # returns diary list as itself to be used
        return self.diary

    def edit_existing(self, edit_details):
        # details for editing once edit has been finalised in edit mode
        edit_cr = edit_details[1]
        edit_data = edit_details[0]

    def export(self):
        with open("data/diary.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.diary)
        input("success")

    def clear(self):
        # overrites the diary with a blank list
        self.diary = []

        # saves blank list, discarding all previous data
        pickle_out = open("data/planner.pickle", "wb")
        pickle.dump(self.diary, pickle_out)
        pickle_out.close()

    def past_show(self):
        # showing events that have been past in time.
        # makin a new variable for past
        past_df = self.past
        # getting the length of the past entries
        past_len = len(past_df)
        # if there are no past entries, No results will be printed
        # and the user will go back to the main menu
        if past_len == 0:
            input("No results")
            pass
        else:
            # the blank list will have empty strings for the data frame index
            blank_list = []
            for blank_str in range(past_len):
                blank_list.append("")

            # plotting to data frame
            past_frame = df(
                past_df,
                index=blank_list, columns=self.column_list
                )

            print(past_frame)

            input(word_strings.strings.enter_menu)

    def clash_delete(self, clash_ind):
        # deletes clashes that the user has chosen from ones that are found
        # in edit mide
        for delete_clashes in clash_ind:
            del self.diary[delete_clashes]

    def delete_entry(self, delete_plan):
        # delete plan from list and save
        del self.diary[delete_plan]

        pickle_out = open("data/planner.pickle", "wb")
        pickle.dump(self.diary, pickle_out)
        pickle_out.close()


# initiate above class
diary_eng = planner()


def edit_mode(existing_entry, entry_number):
    # if there is an existing entry to be edited
    # existing_entry will be True and entry number will be the number
    # in the list to correspond to the index
    # if it is a new entry existing_entry will be False
    # and entry number will have a None value
    def date_entry():
        while True:
            ymd = input()
            # below commented sectionis the skip function which I omitted
            # for the sake of user experience
            # if existing_entry:
            #     if ymd == "":
            #         break
            #     else:
            #         pass
            # else:
            #     pass

            # the length of YYYYMMDD is 8 characters. if 8 characters are
            # inputted, the next section will be allowed to accessed
            if len(ymd) == 8:
                pass
            else:
                print(word_strings.strings.error)
                continue

            try:
                # the above input will be split and coverted to int to be put
                # in the date time format, if any errors happen, the process
                # will raise a value error and will be restarted
                choice_year = int(ymd[0:4])  # year
                choice_month = int(ymd[4:6])  # month
                choice_day = int(ymd[6:8])  # day
                # datetime conversion
                choice_date = dt(choice_year, choice_month, choice_day)
            except ValueError:
                # invalid input string printed
                print(word_strings.strings.error)
                continue

            if choice_date < dt.now():
                # only inputs in the future will be allowed through this input
                print(word_strings.strings.past)
                continue
            else:
                return [choice_year, choice_month, choice_day]

    def time_entry():
        while True:
            min_hour = input()
            # below commented sectionis the skip function which I omitted
            # for the sake of user experience
            # if existing_entry:
            #     if min_hour == "":
            #         time_pass = True
            #         break
            #     else:
            #         pass

            # the length of HHMM is 4 characters. if 4 characters are
            # inputted, the next section will be allowed to accessed
            if len(min_hour) == 4:
                pass
            else:
                print(word_strings.strings.error)
                continue

            try:
                # just like the above function, input will be split and
                # converted to int to be converted to time format
                # any input that is not correct will raise an error and
                # restart this proces
                if 0 <= int(min_hour[0:2]) < 24 and 0 <= int(min_hour[2:4]) < 60:
                    time_pass = False
                    break
                else:
                    print(word_strings.strings.error)
                    continue
            except ValueError:
                print(word_strings.strings.error)

        if not time_pass:
            # returns time values
            return [int(min_hour[0:2]), int(min_hour[2:4])]
        else:
            # returns an empty string if time pass is True
            return ""

    def text_entry(ent_type):
        while True:
            # depending on what the input argument is,
            # the mode is decided on what type of text will be inputted
            text_inp = input()

            # plan is for the plan for an activity and has no restrcitions
            if ent_type == "plan":
                return text_inp

            # priority will only accept specific inputs from low to very high
            # accepted inputs will be adjusted to suit the formatting required
            elif ent_type == "priority":
                prior_key = {
                    "vh": "Very High", "very high": "Very High",
                    "h": "High", "high": "High", "m": "Medium",
                     "medium": "Medium", "l": "Low", "low": "Low"
                     }

                accepted_inputs = [
                        "vh", "h", "m" , "l",
                         "very high", "high",
                         "medium", "low"
                         ]

                # input will be converted to lowercase and adjusted accordingly
                if text_inp.lower() in accepted_inputs:
                    return prior_key[text_inp.lower()]
                else:
                    print(word_strings.strings.error)
                    continue
            # inputs are limited to 15 characters for notes
            elif ent_type == "notes":
                if len(text_inp) <= 15:
                    return text_inp
                else:
                     print(word_strings.strings.max_15)
                     continue

    # if it is an existing entry, you are given the opportunity to
    # change the time, if the option is declined this time options will be
    # skipped
    if existing_entry:
        while True:
            change_time = input("Change times?: ").lower()
            if change_time == "yes" or change_time == "no":
                break
            else:
                print(word_strings.strings.error)
                continue

    # dates will be added here
    if not existing_entry or change_time == "yes":
        print(word_strings.strings.ymd_start + ": ")

        # date 1 entry here
        date_1 = date_entry()
        print(word_strings.strings.time_sel)
        # time entry here
        time_1 = time_entry()

        # time and date goes into datetime variable
        period_1 = dt(
            date_1[0], date_1[1],
            date_1[2], time_1[0],
            time_1[1]
            )

        # period finish time
        print(word_strings.strings.ymd_finish + ":")

        # time and date goes into datetime variable
        while True:
            date_2 = date_entry()
            print(word_strings.strings.time_sel)
            time_2 = time_entry()
            period_2 = dt(
                date_2[0], date_2[1],
                date_2[2], time_2[0],
                time_2[1]
                )

            # if date 2 is before date 1, it will ask to do do that section
            # again
            if date_2 < date_1:
                print(word_strings.strings.past_2)
                continue
            else:
                break

        # dates will be put into the clash function to see if they conflict
        # with any previously made plans in the self.diary list
        clash_process = diary_eng.clash_find(period_1, period_2)

        # if there are no clashes, it will give out a clash_del False
        if not clash_process[0]:
            clash_del = False
            pass
        else:
            print(word_strings.strings.clash_remove)
            while True:
                # the user choses whether they want to allow the clashes
                clash_choice = input().lower()
                if clash_choice == "yes" or clash_choice == "y":
                    clash_del = True
                    break
                elif clash_choice == "no" or clash_choice == "n":
                    clash_del = False
                    break
                else:
                    print(word_strings.strings.error)

        # if no is chosen previously, thie section is skipped
        # if yes is chosen, a loop woll be entered for the user to
        # append a list of the numbers in the list that will be appended
        # with the numbers of the entries to be deleted.
        # if there are no items to delete once the loop is exited
        # both will be kept
        if not clash_del:
            pass
        else:
            list_del = []
            clashes = clash_process[1]
            print(word_strings.strings.remove_indexes)
            while True:
                figure_del = input()
                if figure_del.lower() == "/done":
                    if len(list_del) < 1:
                        clash_del = False
                    else:
                        clash_del = True
                    break
                else:
                    try:
                        figure_int = int(figure_del)
                    except ValueError:
                        print(print(word_strings.strings.error))

                    if figure_int in clashes:
                        list_del.append(figure_int)
                    else:
                        print(word_strings.strings.error)

    else:
        # empty strings will be skipped when edits are made
        period_1 = ""
        period_2 = ""
        pass

    if clash_del:
        list_del.sort()
        list_del.sort(reverse=True)

    # user input is here and functions are used to create vairables
    # for placement in diary entry list
    print("What will happen happen?")
    plan_input = text_entry("plan")
    print("Priority?")
    prior_level = text_entry("priority")
    print("Any extra notes?")
    note_input = text_entry("notes")

    # the choices are given for review, if they are not comfirmed, the process
    # will terminate and the user will be brought back to the main menu
    print("Review")
    print(str(period_1) + " to", str(period_2), plan_input,
        prior_level + " priority.")

    print("Notes:", note_input)
    print("\nTo confirm type 'a' or to return to the menu type 'b'.")
    while True:
        new_confirm = input().lower()
        if new_confirm == "a":
            if clash_del:
                # uses list to delete clash from list
                diary_eng.clash_delete(list_del)
            else:
                pass
            # passes details in the correct format to the class to be saved
            if not existing_entry:
                save_to = [period_1, period_2,
                plan_input, prior_level,
                note_input
                ]
                diary_eng.save_new(save_to)
                new_confirm = True
            elif existing_entry:
                edit_to = [
                    period_1, period_2,
                    plan_input, prior_level,
                    note_input
                    ]
                diary_eng.edit_existing([edit_to, entry_number])
            break

        # sends back to main menu without saving
        elif new_confirm == "b":
            confirm = False
            break
        else:
            print(word_strings.strings.error)
            continue


def show_edit():
    # this function is brought up when view/edit(b) from the main menu
    # is chosen
    full_list = diary_eng.return_type()
    print()
    print(word_strings.strings.edit_opt)
    # True means results are to be sorted in a lambda function
    # False will pass and use another method
    while True:
        show_style = input().lower()
        if show_style == "a":
            return [True, 2]
        elif show_style == "b":
            return [True, 3]
        elif show_style == "c":
            return [True, 4]
        elif show_style == "d":
            return [False, 0]
        elif show_style == "e":
            return [False, 1]
        elif show_style == "g":
            return [False, 2]
        elif show_style == "f":
            return [False, 3]
        else:
            print(word_strings.strings.error)


while True:
    # header
    diary_eng.header("Main Menu")
    print(word_strings.strings.main_menu)

    menu_choice = input().lower()
    if menu_choice == "a":
        # this controls what is presented in the header
        diary_eng.header("New entry")
        edit_mode(False, None)

    elif menu_choice == "b":
        # column list for the dataframe to correspond with the diary list
        col_list = ["Start", "Finish", "Plan", "Priority", "Notes"]
        diary_eng.header("View and edit entries")
        allow_edit = diary_eng.showing_results()
        # if there are no results to show it will go back to the main menu
        if allow_edit:
            view_type = show_edit()
            # diary is returned from class function here.
            t_diary = diary_eng.return_type()
            if view_type[0]:

                sort_value = view_type[1]
                sort_func = lambda plan_l: plan_l[sort_value]
                t_diary.sort(key=sort_func)
                sr_len = len(t_diary)

                # makes an empty list for strings
                str_emptylist = [""]*sr_len

                # dataframe for sorted entries
                srt_df = df(t_diary, index=str_emptylist, columns=col_list)

                print(srt_df)
                print("**")
                input(word_strings.strings.enter_menu)

            else:
                if view_type[1] == 0:
                    while True:
                        # resuts go here from search
                        search_results = []
                        search_yeilda = []
                        yeild_index = []
                        search_query = input(word_strings.strings.search_text).lower()
                        full_len = len(t_diary)

                        # will send to the main menu, otherwise loop will
                        # continue
                        if search_query == "/back":
                            break
                        elif search_query == "":
                            continue

                        # loop to use query to find entries that have
                        # matches will be chosen if a part of the query input
                        # is in the current string for diary entry
                        for search_yeild in range(full_len):
                            query_low = t_diary[search_yeild][2].lower()
                            if search_query in query_low:
                                search_results.append(search_yeild)
                            else:
                                pass

                        # all indexes are places for the index section of
                        # the dataframe
                        for yeild_results in search_results:
                            yeild_index.append(yeild_results)
                            search_yeilda.append(t_diary[yeild_results])

                        result_counter = str(len(yeild_index))
                        print("---")
                        print(result_counter + " result(s) found")
                        print()
                        if len(yeild_index) == 0:
                            continue

                        # omitted function for
                        # for abbr in range(len(search_yeilda)):
                        #     if search_yeilda[abbr][0].strftime("%A %d %B %Y") == search_yeilda[abbr][1].strftime("%A %d %B %Y"):
                        #         new_date = search_yeilda[abbr][1].strftime("%X")
                        #         search_yeilda[abbr][1] = new_date

                        # dataframe from search results
                        search_df = df(
                            search_yeilda,
                            index=yeild_index, columns=col_list
                            )

                        print(search_df)
                        print()
                    continue

                if view_type[1] == 1:
                    # preparing for edit mode
                    di_len = len(t_diary)
                    # list of indexes
                    ind_list = []
                    for number_index in range(di_len):
                        ind_list.append(number_index)
                    print("Choose and entry number to edit")
                    while True:
                        try:
                            edit_index = int(input())
                        except ValueError:
                            print(word_strings.strings.error)
                            continue
                        if edit_index in ind_list:
                            edit_mode(True, edit_index)
                            break
                        else:
                            print(word_strings.strings.error)
                            continue

                if view_type[1] == 3:
                    # user will be promoted to choose an index of the
                    # entry number before confirming it to be deleted
                    # all invalid inputs will be declined and the loop
                    # will be reset
                    print(word_strings.strings.choose_delete)
                    in_list = []
                    for del_numbers in range(len(t_diary)):
                        in_list.append(del_numbers)
                    while True:
                        delete_number = input()

                        if delete_number == "/back":
                            break
                        try:
                            delete_int = int(delete_number)
                        except ValueError:
                            print(word_strings.strings.error)
                            continue

                        if delete_int in in_list:
                            break
                        else:
                            print(word_strings.strings.error)
                            continue

                    while True:
                        c_del = input(word_strings.strings.confirm_delete)
                        if c_del.lower() in ["yes", "y"]:
                            diary_eng.delete_entry(delete_int)
                            input("Success! \n")
                            break
                        elif c_del.lower() in ["no", "no"]:
                            break

        else:
            print(word_strings.strings.enter_menu)
            input("")

    elif menu_choice == "c":
        # exports all entries to csv in the data folder
        diary_eng.export()
    elif menu_choice == "d":
        # gives the user the options to completely clear the list
        print("Are you sure you want to clear all upcoming plans?")
        # user is prompted before this happens
        while True:
            all_del = input().lower()
            if all_del in ["yes", "y"]:
                diary_eng.clear()
                input("Success")
                break
            if all_del in ["no", "n"]:
                break
            else:
                print(word_strings.strings.error)
                continue
    elif menu_choice == "e":
        diary_eng.past_show()
        # showing past entries in a dataframe
    elif menu_choice == "f":
        # shows credits
        for credit_reel in word_strings.strings.credits:
            print(credit_reel)
            # 1.5 second gap between printing lines
            sleep(1.5)
        input("Thank you and enjoy!")
    elif menu_choice == "g":
        # exits the program
        exit()

# end
