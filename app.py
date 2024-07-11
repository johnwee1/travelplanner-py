import streamlit as st
import datetime
import query


def get_date_range(selected_date):
    start_date = selected_date - datetime.timedelta(days=10)
    end_date = selected_date + datetime.timedelta(days=10)
    return start_date, end_date


def is_available(date, available_dates):
    return date.strftime("%d/%m/%y") in available_dates


def move_left(index):
    st.session_state.selected_users.insert(
        index - 1, st.session_state.selected_users.pop(index)
    )


def move_right(index):
    st.session_state.selected_users.insert(
        index + 1, st.session_state.selected_users.pop(index)
    )


def render_user_column(user, index, total_users):
    if index == 0:
        sc1, sc2 = st.columns(2)
        sc1.write(user)
        sc2.button("➡", key=f"{user}_right", on_click=move_right, args=(index,))
    elif index == total_users - 1:
        sc1, sc2 = st.columns(2)
        sc1.button("⬅", key=f"{user}_left", on_click=move_left, args=(index,))
        sc2.write(user)
    else:
        sc1, sc2, sc3 = st.columns(3)
        sc1.button("⬅", key=f"{user}_left", on_click=move_left, args=(index,))
        sc2.write(user)
        sc3.button("➡", key=f"{user}_right", on_click=move_right, args=(index,))


def render_availability_calendar(date_range, person):
    for date in date_range:
        color = "green" if is_available(date, person.available_dates) else "white"
        st.markdown(
            f"""
            <span style="
                display: inline-block;
                width: 60px;
                height: 60px;
                border-radius: 10px;
                background-color: {color};
                color: #474747;
                font-size: 24px;
                line-height: 60px;
                text-align: center;
                font-weight: bold;
                margin: 5px;
            ">{date.day}</span>
            """,
            unsafe_allow_html=True,
        )


def render_user_availabilities(selected_users, date_range, Persons):
    columns = st.columns(
        len(st.session_state.selected_users), vertical_alignment="bottom"
    )
    for i, user in enumerate(st.session_state.selected_users):
        with columns[i]:
            render_user_column(user, i, len(st.session_state.selected_users))
            render_availability_calendar(date_range, Persons[user])


def main():
    st.title("Availability Checker")

    url = st.text_input("Enter the URL of the Google Sheets document")
    retrieve_data = st.button("Retrieve Data")

    if "Persons" not in st.session_state:
        st.session_state.Persons = None

    if "selected_users" not in st.session_state:
        st.session_state.selected_users = []

    if retrieve_data:
        st.session_state.Persons = query.retrieve_db(url)

    if st.session_state.Persons:
        selected_date = st.date_input("Select a date", datetime.date.today())
        st.session_state.selected_users = st.multiselect(
            "Select users",
            list(st.session_state.Persons.keys()),
            default=st.session_state.selected_users,
        )

        if st.session_state.selected_users:
            start_date, end_date = get_date_range(selected_date)
            date_range = [
                start_date + datetime.timedelta(days=x)
                for x in range((end_date - start_date).days + 1)
            ]
            render_user_availabilities(
                st.session_state.selected_users, date_range, st.session_state.Persons
            )


if __name__ == "__main__":
    main()
