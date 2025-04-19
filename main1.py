import streamlit as st
import requests
import re
import plotly.express as px

BASE_URL = "http://localhost:8000"  # FastAPI backend


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def main():
    st.set_page_config(page_title="CRUD App", page_icon="🛠️")
    st.title("🧑‍💻 User CRUD Application")

    tabs = st.tabs(["Create", "Read", "Update", "Delete"])

    # ----------------- Create Tab -----------------
    with tabs[0]:
        st.subheader("➕ Create a New User")
        name = st.text_input("👤 Name")
        email = st.text_input("📧 Email")

        if st.button("Create User"):
            if not name or not email:
                st.warning("⚠️ Please fill in both name and email.")
            elif not is_valid_email(email):
                st.error("❌ Enter a valid email address.")
            else:
                with st.spinner("Creating user..."):
                    payload = {"name": name, "email": email}
                    response = requests.post(f"{BASE_URL}/users", json=payload)
                    if response.status_code == 200:
                        st.success("✅ User created successfully!")
                    else:
                        st.error(
                            f"❌ Error: {response.json().get('detail', 'Unknown error')}"
                        )

    # ----------------- Read Tab -----------------
    with tabs[1]:
        st.subheader("📖 All Users")
        if st.button("🔄 Refresh Users"):
            response = requests.get(f"{BASE_URL}/users")
            if response.status_code == 200:
                users = response.json()
                if users:
                    st.dataframe(users, use_container_width=True)
                    st.markdown("### 📊 Stats")
                    col1, col2 = st.columns(2)
                    col1.metric("Total Users", len(users))
                    col2.metric("Total Columns", len(users[0]) if users else 0)
                    # Bar chart with axis labels
                    chart_data = {
                        "Metric": ["Total Users", "Total Columns"],
                        "Count": [len(users), len(users[0]) if users else 0],
                    }
                    fig = px.bar(
                        chart_data,
                        x="Metric",
                        y="Count",
                        text="Count",
                        title="User Table Summary",
                    )
                    fig.update_traces(
                        marker_color=["#1f77b4", "#ff7f0e"], textposition="outside"
                    )
                    fig.update_layout(
                        xaxis_title="Metric", yaxis_title="Count", showlegend=False
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("ℹ️ No users found.")
            else:
                st.error("❌ Failed to fetch users")

    # ----------------- Update Tab -----------------
    with tabs[2]:
        st.subheader("✏️ Update User")
        user_id = st.number_input("🆔 User ID", min_value=1)
        new_name = st.text_input("🔁 New Name")
        new_email = st.text_input("📧 New Email")

        if st.button("Update User"):
            if not new_name or not new_email:
                st.warning("⚠️ Fill in both fields to update.")
            elif not is_valid_email(new_email):
                st.error("❌ Invalid email format.")
            else:
                payload = {"name": new_name, "email": new_email}
                response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)
                if response.status_code == 200:
                    st.success("✅ User updated successfully!")
                else:
                    st.error(f"❌ Error: {response.json().get('detail')}")

    # ----------------- Delete Tab -----------------
    with tabs[3]:
        st.subheader("🗑️ Delete User")
        del_id = st.number_input("Enter ID to delete", min_value=1, key="delete_id")
        if st.button("Delete User"):
            response = requests.delete(f"{BASE_URL}/users/{del_id}")
            if response.status_code == 200:
                st.success("🗑️ User deleted successfully!")
            else:
                st.error(f"❌ Error: {response.json().get('detail')}")


if __name__ == "__main__":
    main()
