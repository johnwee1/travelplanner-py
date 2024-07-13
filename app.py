import streamlit as st
import datetime
import query


def get_date_range(selected_date, n):
    start_date = selected_date - datetime.timedelta(days=n)
    end_date = selected_date + datetime.timedelta(days=n)
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


def render_availability_calendar(date_range, user):
    for date in date_range:
        color = (
            "#54ff82" if is_available(date, st.session_state.db[user]) else "#242424"
        )
        st.markdown(
            f"""
            <span style="
                display: inline-block;
                width: 60px;
                height: 60px;
                border-radius: 6px;
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


def render_user_availabilities(date_range):
    columns = st.columns(
        len(st.session_state.selected_users), vertical_alignment="bottom"
    )
    for i, user in enumerate(st.session_state.selected_users):
        with columns[i]:
            render_user_column(user, i, len(st.session_state.selected_users))
            render_availability_calendar(date_range, user)


def main():
    st.title("Availability Checker")
    st.write(
        "Having trouble planning something with friends? Here's the solution nobody asked for!"
    )
    st.write(
        "Note: Your Google form WILL need the fields 'name' and 'availabilities' for this to work. Also yeah its case-sensitive, smaller case only."
    )
    url = st.text_input(
        "Enter the URL of the Google Sheets document you want to visualize!"
    )
    retrieve_data = st.button("Get Started")

    if "db" not in st.session_state:
        st.session_state.db = None

    if "selected_users" not in st.session_state:
        st.session_state.selected_users = []

    if retrieve_data:
        st.session_state.db = query.retrieve_db(url)

    if st.session_state.db:
        show_db = st.checkbox(label="Show all users", value=False)
        if show_db:
            st.dataframe(st.session_state.db)

        selected_date = st.date_input("Select a date to check", datetime.date.today())

        st.session_state.selected_users = st.multiselect(
            "Select users",
            list(st.session_state.db.keys()),
            default=st.session_state.selected_users,
        )

        if "interval" not in st.session_state:
            st.session_state.interval = 10

        interval = st.number_input(
            label="The number of days out from the day specified to display",
            min_value=1,
            max_value=30,
            value=st.session_state.interval,
        )

        if st.session_state.selected_users:
            start_date, end_date = get_date_range(selected_date, interval)
            date_range = [
                start_date + datetime.timedelta(days=i)
                for i in range((end_date - start_date).days + 1)
            ]
            render_user_availabilities(date_range)


if __name__ == "__main__":
    main()
