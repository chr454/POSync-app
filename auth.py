
import streamlit as st
from supabase import create_client


def get_supabase_client():
    """Create and return a Supabase client for this Streamlit session."""
    if "posync_supabase" not in st.session_state:
        try:
            supabase_url = st.secrets["SUPABASE_URL"]
            supabase_key = st.secrets["SUPABASE_KEY"]
        except KeyError as exc:
            raise RuntimeError(
                "Supabase configuration is missing. "
                "Check Streamlit Secrets."
            ) from exc

        st.session_state["posync_supabase"] = create_client(
            supabase_url,
            supabase_key
        )

    return st.session_state["posync_supabase"]


def login(email: str, password: str):
    """Authenticate a user and load their POSync profile."""
    email = email.strip()

    if not email or not password:
        return False, "Please enter both your email and password."

    try:
        supabase = get_supabase_client()

        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not auth_response.user or not auth_response.session:
            return False, "Login failed. Please check your details."

        user_id = auth_response.user.id

        profile_response = (
            supabase.table("profiles")
            .select("user_id, business_id, role, full_name")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        profiles = profile_response.data or []

        if not profiles:
            supabase.auth.sign_out()
            return (
                False,
                "Your account is not linked to a POSync business. "
                "Please contact the business owner."
            )

        profile = profiles[0]
        role = profile.get("role")

        if role not in ("owner", "staff"):
            supabase.auth.sign_out()
            return False, "Your POSync account has an invalid role."

        st.session_state["posync_user"] = {
            "id": user_id,
            "email": auth_response.user.email or email,
            "business_id": profile["business_id"],
            "role": role,
            "full_name": profile.get("full_name"),
        }

        return True, "Login successful."

    except Exception:
        return (
            False,
            "Login failed. Check your details and connection, "
            "then try again. If the problem continues, "
            "contact the POSync administrator."
        )


def logout():
    """Sign out the current user and clear POSync authentication state."""
    supabase = st.session_state.get("posync_supabase")

    if supabase is not None:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

    for key in ("posync_user", "posync_supabase"):
        st.session_state.pop(key, None)


def current_user():
    """Return the authenticated POSync user profile, or None."""
    return st.session_state.get("posync_user")


def is_authenticated():
    """Check whether this Streamlit session has a POSync user."""
    return current_user() is not None


def require_auth(allowed_roles=None):
    """Protect a page from unauthenticated or unauthorized access."""
    user = current_user()

    if user is None:
        st.warning("Please log in to access POSync.")
        st.stop()

    if allowed_roles and user.get("role") not in allowed_roles:
        st.error("You do not have permission to access this page.")
        st.stop()

    return user


def render_login():
    """Display the POSync login form."""
    st.title("POSync Login")
    st.write("Sign in with your business account to continue.")

    with st.form("posync_login_form"):
        email = st.text_input(
            "Email address",
            placeholder="name@example.com"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Log in",
            use_container_width=True
        )

    if submitted:
        success, message = login(email, password)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
