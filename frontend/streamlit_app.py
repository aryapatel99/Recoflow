from __future__ import annotations

import uuid

import requests
import streamlit as st


API_URL = st.sidebar.text_input(
    "API URL",
    value="http://127.0.0.1:8000",
)


st.set_page_config(
    page_title="RecoFlow",
    page_icon="🛍️",
    layout="wide",
)


def api_request(
    method: str,
    path: str,
    token: str | None = None,
    json: dict | None = None,
):
    headers = {}

    if token:
        headers["Authorization"] = (
            f"Bearer {token}"
        )

    try:
        response = requests.request(
            method=method,
            url=f"{API_URL}{path}",
            headers=headers,
            json=json,
            timeout=15,
        )

        return response

    except requests.RequestException as exc:
        st.error(
            f"Backend connection failed: {exc}"
        )
        return None


def extract_items(data):
    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    for key in (
        "items",
        "products",
        "data",
        "results",
    ):
        value = data.get(key)

        if isinstance(value, list):
            return value

    return []


def login():
    st.subheader("Login")

    email = st.text_input(
        "Email",
        key="login_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
    )

    if st.button(
        "Login",
        type="primary",
    ):
        response = api_request(
            "POST",
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        if response is None:
            return

        if response.status_code == 200:
            data = response.json()

            st.session_state.token = (
                data.get("access_token")
            )

            st.session_state.logged_in = True

            st.success("Login successful.")

            st.rerun()

        else:
            st.error(
                response.text
            )


def register():
    st.subheader("Create account")

    full_name = st.text_input(
        "Full name",
        key="register_name",
    )

    email = st.text_input(
        "Email",
        key="register_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password",
    )

    if st.button("Create account"):
        response = api_request(
            "POST",
            "/auth/register",
            json={
                "full_name": full_name,
                "email": email,
                "password": password,
            },
        )

        if response is None:
            return

        if response.status_code in (
            200,
            201,
        ):
            data = response.json()

            st.success(
                "Account created."
            )


        else:
            st.error(
                response.text
            )


def send_event(
    event_type: str,
    product_id: int,
):
    token = st.session_state.get(
        "token"
    )

    if not token:
        return

    payload = {
        "event_type": event_type,
        "product_id": product_id,
        "session_id": st.session_state.get(
            "session_id"
        ),
        "metadata": {
            "source": "streamlit",
        },
    }

    response = api_request(
        "POST",
        "/api/v1/events",
        token=token,
        json=payload,
    )

    if response is not None and response.status_code not in (
        200,
        201,
    ):
        st.warning(
            f"Event failed: {response.text}"
        )


def load_products():
    response = api_request(
        "GET",
        "/api/v1/products?limit=50",
    )

    if response is None:
        return []

    if response.status_code != 200:
        st.error(
            response.text
        )
        return []

    return extract_items(
        response.json()
    )


def load_recommendations():
    token = st.session_state.get(
        "token"
    )

    if not token:
        return []

    response = api_request(
        "GET",
        "/api/v1/recommendations/hybrid?limit=12",
        token=token,
    )

    if response is None:
        return []

    if response.status_code != 200:
        st.warning(
            response.text
        )
        return []

    data = response.json()

    return extract_items(data)


def product_card(product):
    product_id = product.get(
        "product_id",
        product.get("id"),
    )

    title = product.get(
        "title",
        "Product",
    )

    price = product.get(
        "price",
        0,
    )

    brand = product.get(
        "brand",
        "",
    )

    rating = product.get(
        "rating",
        0,
    )

    st.markdown(
        f"### {title}"
    )

    if brand:
        st.caption(
            f"{brand}"
        )

    st.write(
        f"₹{price:,.2f}"
    )

    if rating:
        st.write(
            f"⭐ {rating}"
        )

    if product_id is not None:
        if st.button(
            "View",
            key=f"view_{product_id}",
        ):
            send_event(
                "product_view",
                int(product_id),
            )

        if st.button(
            "Add to cart",
            key=f"cart_{product_id}",
        ):
            send_event(
                "add_to_cart",
                int(product_id),
            )

            st.success(
                "Added to cart event recorded."
            )


def shopping_page():
    st.title(
        "🛍️ RecoFlow"
    )

    st.caption(
        "Personalized recommendation and ranking platform"
    )

    recommendations = load_recommendations()

    if recommendations:
        st.header(
            "Recommended for you"
        )

        columns = st.columns(4)

        for index, product in enumerate(
            recommendations
        ):
            with columns[index % 4]:
                product_card(product)

    st.divider()

    st.header(
        "Product Catalog"
    )

    products = load_products()

    if not products:
        st.info(
            "No products available. "
            "Seed the catalog first."
        )
        return

    search = st.text_input(
        "Search products",
    )

    if search:
        products = [
            product
            for product in products
            if search.lower()
            in str(
                product.get(
                    "title",
                    "",
                )
            ).lower()
        ]

    columns = st.columns(4)

    for index, product in enumerate(
        products
    ):
        with columns[index % 4]:
            product_card(product)


def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(
            uuid.uuid4()
        )

    st.sidebar.title(
        "RecoFlow"
    )

    if st.session_state.logged_in:
        if st.sidebar.button(
            "Logout"
        ):
            st.session_state.clear()
            st.rerun()

        shopping_page()

    else:
        tab_login, tab_register = st.tabs(
            [
                "Login",
                "Register",
            ]
        )

        with tab_login:
            login()

        with tab_register:
            register()

        st.divider()

        st.info("Create an account, then sign in immediately.")


if __name__ == "__main__":
    main()