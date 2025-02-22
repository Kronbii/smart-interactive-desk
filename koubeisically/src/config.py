# ----------------------- Flags -----------------------
ds4_control = True
web_control = True
manual_control = False
auto_control = False

# ----------------------- User Info -----------------------
user_id = 000
user_name = "koubeisically"
user_pref_height = 120


# ----------------------- Misc -----------------------
if auto_control:
    ds4_control = False
    web_control = False
    manual_control = False

elif manual_control:
    ds4_control = False
    web_control = False
    auto_control = False