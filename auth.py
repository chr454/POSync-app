
        profiles = profile_response.data or []

        if not profiles:
            supabase.auth.sign_out()
            return (
                False,
                "Your account is not linked to a POSync business. "
                "Please contact the business owner.",
            )

        profile = profiles[0]
        role = profile.get("role")

        if role not in ("owner", "staff"):
            supabase.auth.sign_out()
            return False, "Your POSync account has an invalid role."

        # Keep only non-secret user/profile details in Streamlit session state.
        # The Supabase client retains the authenticated session for this
        # Streamlit browser session.
        st.session_state["posync_user"] = {
            "id": user_id,
            "email": auth_response.user.email or email,
            "business_id": profile["business_id"],
            "role": role,
            "full_name": profile.get("full_name"),
        }

        return True, "Login successful."

    except Exception:
        # Avoid displaying raw authentication/database exceptions to users.
        return (
            False,
            "Login failed. Check your details and connection, then try again. "
            "If the problem continues, contact the POSync administrator.",
        )


def logout():
    """Sign out the current user and clear POSync authentication state."""
    supabase = st.session_state.get("posync_supabase")

    if supabase is not None:
        try:
            supabase.auth.sign_out()
        except Exception:
            # Clear the local app session even if the remote sign-out fails.
            pass

    for key in (
        "posync_user",
        "posync_supabase",
    ):
        st.session_state.pop(key, None)


def current_user():
    """Return the authenticated POSync user profile, or None."""
    return st.session_state.get("posync_user")


def is_authenticated():
    """Check whether this Streamlit session has a POSync user."""
    return current_user() is not None


def require_auth(allowed_roles=None):
    """
    Protect a page from unauthenticated access.

    Call this near the top of every file in the pages/ directory.
    Optionally pass allowed_roles, e.g. ["owner"].
    """
    user = current_user()

    if user is None:
        st.warning("Please log in to access POSync.")
        st.stop()

    if allowed_roles and user.get("role") not in allowed_roles:
        st.error("You do not have permission to access this page.")
        st.stop()

    return user


def render_login():
    """Display the POSync login form on the home page."""
    st.title("POSync Login")
    st.write("Sign in with your business account to continue.")

    with st.form("posync_login_form"):
        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
        )
        password = st.text_input(
            "Password",
            type="password",
        )
        submitted = st.form_submit_button(
            "Log in",
            use_container_width=True,
        )

    if submitted:
        success, message = login(email, password)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
