"""
Admin dashboard components
"""
import streamlit as st
import pandas as pd
from database.user_db_manager import UserDatabaseManager
from database.db_manager import DatabaseManager
from services import ComplaintService


def render_admin_dashboard():
    """Render admin dashboard for user and complaint management"""
    st.title("⚙️ Admin Dashboard")
    
    tabs = st.tabs(["👥 User Management", "📊 System Statistics", "🔧 Bulk Operations"])
    
    # Tab 1: User Management
    with tabs[0]:
        render_user_management()
    
    # Tab 2: System Statistics
    with tabs[1]:
        render_system_stats()
    
    # Tab 3: Bulk Operations
    with tabs[2]:
        render_bulk_operations()


def render_user_management():
    """Render user management interface"""
    st.subheader("👥 User Management")
    
    user_db = UserDatabaseManager()
    users = user_db.get_all_users()
    
    if not users:
        st.info("No users found")
        return
    
    # Display users in a table
    user_data = []
    for user in users:
        user_data.append({
            'ID': user.id,
            'Username': user.username,
            'Full Name': user.full_name,
            'Email': user.email,
            'Role': user.role.upper(),
            'Status': '✅ Active' if user.is_active else '❌ Inactive',
            'Created': user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'
        })
    
    df = pd.DataFrame(user_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # User Actions
    st.subheader("🔧 User Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Change User Role")
        selected_user_id = st.selectbox(
            "Select User",
            options=[u.id for u in users],
            format_func=lambda x: f"{next(u.username for u in users if u.id == x)} ({next(u.role for u in users if u.id == x)})"
        )
        
        new_role = st.selectbox(
            "New Role",
            options=["citizen", "moderator", "admin"]
        )
        
        if st.button("✅ Update Role", use_container_width=True):
            if user_db.update_user_role(selected_user_id, new_role):
                st.success(f"✅ Role updated to {new_role}")
                st.rerun()
            else:
                st.error("❌ Failed to update role")
    
    with col2:
        st.markdown("##### Activate/Deactivate User")
        action_user_id = st.selectbox(
            "Select User ",
            options=[u.id for u in users],
            format_func=lambda x: f"{next(u.username for u in users if u.id == x)} ({'Active' if next(u.is_active for u in users if u.id == x) else 'Inactive'})",
            key="action_user"
        )
        
        selected_user = next(u for u in users if u.id == action_user_id)
        
        if selected_user.is_active:
            if st.button("❌ Deactivate User", use_container_width=True):
                if user_db.deactivate_user(action_user_id):
                    st.success("✅ User deactivated")
                    st.rerun()
        else:
            if st.button("✅ Activate User", use_container_width=True):
                if user_db.activate_user(action_user_id):
                    st.success("✅ User activated")
                    st.rerun()


def render_system_stats():
    """Render system statistics"""
    st.subheader("📊 System Statistics")
    
    user_db = UserDatabaseManager()
    db = DatabaseManager()
    
    users = user_db.get_all_users()
    
    # User statistics
    total_users = len(users)
    active_users = len([u for u in users if u.is_active])
    admins = len([u for u in users if u.role == 'admin'])
    moderators = len([u for u in users if u.role == 'moderator'])
    citizens = len([u for u in users if u.role == 'citizen'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total Users", total_users)
    col2.metric("Active Users", active_users)
    col3.metric("Admins", admins)
    col4.metric("Moderators", moderators)
    col5.metric("Citizens", citizens)
    
    st.markdown("---")
    
    # Complaint statistics
    service = ComplaintService()
    stats = db.get_statistics()
    
    st.markdown("### 📋 Complaint Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Complaints", stats['total'])
    col2.metric("Pending", stats['by_status'].get('pending', 0))
    col3.metric("In Progress", stats['by_status'].get('in_progress', 0))
    col4.metric("Resolved", stats['by_status'].get('resolved', 0))
    
    # User activity
    st.markdown("---")
    st.markdown("### 👤 User Activity")
    
    user_activity = []
    for user in users:
        complaints = db.get_complaints_by_user(user.id)
        user_activity.append({
            'Username': user.username,
            'Full Name': user.full_name,
            'Role': user.role,
            'Complaints Submitted': len(complaints),
            'Active': '✅' if user.is_active else '❌'
        })
    
    df_activity = pd.DataFrame(user_activity)
    df_activity = df_activity.sort_values('Complaints Submitted', ascending=False)
    st.dataframe(df_activity, use_container_width=True, hide_index=True)


def render_bulk_operations():
    """Render bulk operations interface"""
    st.subheader("🔧 Bulk Operations")
    
    st.warning("⚠️ These operations affect multiple records. Use with caution!")
    
    db = DatabaseManager()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Bulk Status Update")
        st.info("Update status for all complaints with a specific current status")
        
        from_status = st.selectbox(
            "From Status",
            options=["pending", "in_progress", "resolved", "rejected"]
        )
        
        to_status = st.selectbox(
            "To Status",
            options=["pending", "in_progress", "resolved", "rejected"],
            key="to_status"
        )
        
        if st.button("🔄 Update All", use_container_width=True):
            # Get complaints with from_status
            complaints = db.get_complaints_by_status(from_status)
            count = 0
            for complaint in complaints:
                if db.update_status(complaint.id, to_status):
                    count += 1
            
            st.success(f"✅ Updated {count} complaints from '{from_status}' to '{to_status}'")
    
    with col2:
        st.markdown("#### 🗑️ Data Cleanup")
        st.info("Clean up old resolved complaints")
        
        days_old = st.number_input(
            "Delete resolved complaints older than (days)",
            min_value=30,
            max_value=365,
            value=90
        )
        
        if st.button("🗑️ Clean Old Records", use_container_width=True, type="secondary"):
            st.warning("This feature will be implemented with proper confirmation dialog")
    
    st.markdown("---")
    
    # Assignment operations
    st.markdown("#### 👨‍💼 Bulk Assignment")
    
    user_db = UserDatabaseManager()
    moderators = [u for u in user_db.get_all_users() if u.role in ['moderator', 'admin']]
    
    if moderators:
        assign_to = st.selectbox(
            "Assign to Moderator/Admin",
            options=[m.id for m in moderators],
            format_func=lambda x: f"{next(m.full_name for m in moderators if m.id == x)} ({next(m.role for m in moderators if m.id == x)})"
        )
        
        assignment_filter = st.selectbox(
            "Assign complaints that are",
            options=["All Pending", "All Unassigned", "Specific Tag"]
        )
        
        if st.button("📌 Assign Complaints", use_container_width=True):
            current_user = st.session_state.user
            complaints = []
            
            if assignment_filter == "All Pending":
                complaints = db.get_complaints_by_status("pending")
            elif assignment_filter == "All Unassigned":
                # Get all complaints where assigned_to is None
                all_complaints = db.get_all_complaints(limit=1000)
                complaints = [c for c in all_complaints if not c.assigned_to]
            
            count = 0
            for complaint in complaints:
                if db.assign_complaint(complaint.id, assign_to, current_user.id):
                    count += 1
            
            st.success(f"✅ Assigned {count} complaints")
    else:
        st.info("No moderators or admins available for assignment")


def render_moderator_panel():
    """Render moderator panel - simplified version of admin dashboard"""
    st.title("🛡️ Moderator Panel")
    
    tabs = st.tabs(["📋 My Assigned Complaints", "✅ Quick Actions"])
    
    current_user = st.session_state.user
    db = DatabaseManager()
    
    with tabs[0]:
        st.subheader("📋 Complaints Assigned to Me")
        
        # Get all complaints assigned to this moderator
        all_complaints = db.get_all_complaints(limit=1000)
        my_complaints = [c for c in all_complaints if c.assigned_to == current_user.id]
        
        if my_complaints:
            for complaint in my_complaints:
                with st.expander(f"Complaint #{complaint.id} - {complaint.location} ({complaint.status})"):
                    st.write(f"**Description:** {complaint.description}")
                    st.write(f"**Tags:** {complaint.tags}")
                    st.write(f"**Created:** {complaint.created_at}")
                    
                    new_status = st.selectbox(
                        "Update Status",
                        options=["pending", "in_progress", "resolved", "rejected"],
                        index=["pending", "in_progress", "resolved", "rejected"].index(complaint.status),
                        key=f"status_{complaint.id}"
                    )
                    
                    if st.button(f"✅ Update Status for #{complaint.id}", key=f"update_{complaint.id}"):
                        if db.update_status(complaint.id, new_status):
                            st.success(f"✅ Status updated to {new_status}")
                            st.rerun()
        else:
            st.info("No complaints assigned to you yet")
    
    with tabs[1]:
        st.subheader("✅ Quick Actions")
        
        st.info("Quick access to common moderation tasks")
        
        # Recent pending complaints
        pending = db.get_complaints_by_status("pending")
        
        st.write(f"**{len(pending)} Pending Complaints**")
        
        if pending:
            for complaint in pending[:5]:  # Show first 5
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"#{complaint.id}: {complaint.location}")
                with col2:
                    if st.button("✅ Accept", key=f"accept_{complaint.id}"):
                        db.assign_complaint(complaint.id, current_user.id, current_user.id)
                        db.update_status(complaint.id, "in_progress")
                        st.success("Accepted!")
                        st.rerun()
                with col3:
                    if st.button("❌ Reject", key=f"reject_{complaint.id}"):
                        db.update_status(complaint.id, "rejected")
                        st.success("Rejected!")
                        st.rerun()
