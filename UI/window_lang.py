class MT(object):
    """MAIN WINDOW TEXT"""

    window_title = {"EN": "AURORA CLEARING", "CN": "极光清算"}


class LT(object):
    """LOGIN WINDOW TEXT"""

    window_title = {"EN": "LOGIN WINDOW", "CN": "登录"}
    button_term = {"EN": "PLEASE AGREE WITH TERMS", "CN": "请同意条款"}
    button_login = {"EN": "LOGIN", "CN": "登录"}
    username = {"EN": "Username", "CN": "用户名"}
    password = {"EN": "Password", "CN": "密码"}
    settings = {"EN": "Settings", "CN": "设置"}
    ip = {"EN": "Server IP", "CN": "服务器IP"}
    port = {"EN": "Server Port", "CN": "服务器端口"}
    submit = {"EN": "Submit", "CN": "提交"}
    reset = {"EN": "Reset", "CN": "重置"}


class BT(object):
    """BROKER WINDOW TEXT"""

    window_title = {"EN": "ADD BROKER ACCOUNT", "CN": "添加券商账户"}
    group_add = {"EN": "Add New Account", "CN": "添加新的账户"}
    group_verify = {"EN": "Verify Local Account", "CN": "验证本地账户"}
    group_delete = {"EN": "Delete Account", "CN": "删除账户"}
    label_verify = {"EN": "Fetch and verify local account", "CN": "获取并验证本地账户"}
    button_verify = {"EN": "Verify", "CN": "验证"}
    label_verified_acc = {"EN": "Verified Accounts", "CN": "验证成功的账户"}
    label_delete = {
        "EN": "Please input ID from the above list to delete",
        "CN": "请输入列表中的ID来删除",
    }
    button_delete = {"EN": "Delete", "CN": "删除"}
    label_delete_all = {"EN": "Delete all local accounts", "CN": "删除所有本地账户"}
    button_delete_all = {"EN": "Delete Local Accounts", "CN": "删除本地账户"}
    label_add = {"EN": "Please choose broker", "CN": "请选择券商"}
    label_username = {"EN": "Username", "CN": "用户名"}
    label_pass = {"EN": "Password", "CN": "密码"}
    # "https://risk.futuhk.com/risk-disclosure/openapi-disclaimer"><span style=" text-decoration: underline; color:#0000ff;">Disclaimer1</span></a><a href="https://www.futunn.com/about/api-disclaimer">
    label_disclaimer = {
        "EN": [
            "Please Login FutuOpenD and",
            "finish the Disclaimer before using our system",
        ],
        "CN": ["请在使用本系统前登录FutuOpenD网关", "并完成API免责条款"],
    }
    button_get_acc = {"EN": "Get Account List", "CN": "获取交易账户列表"}
    label_select_acc = {"EN": "Please select an account to add", "CN": "请选择一个账户添加"}
    label_trading_pass = {"EN": "Trading Password", "CN": "交易密码"}
    button_add = {"EN": "Add Account", "CN": "添加账户"}
    acc_getter_failed = {
        "EN": ["Failed to Get Account List", "Please Check Your FutuOpenD."],
        "CN": ["获取账户列表失败", "请检查您的FutuOpenD网关是否登录"],
    }
    button_text = {"EN": "Add", "CN": ""}


class L1T(object):
    """LEVEL ONE WINDOW TEXT"""

    window_title = {"EN": "LEVEL ONE", "CN": "LEVEL ONE"}


class MOT(object):
    """MODIFY ORDER TEXT"""

    window_title = {"EN": "MODIFY ORDER", "CN": "修改订单"}


class PST(object):
    """POSITION SUMMARY TEXT"""

    window_title = {"EN": "POSITION SUMMARY", "CN": "持仓"}
    label_chooseAccount = {
        "EN": "Please double click from the list to choose an account",
        "CN": "双击左侧列表选择一个账户显示",
    }
    account_list_widget = {"EN": "All Accounts", "CN": "所有账户"}
    table_columns = {
        "EN": [
            "ACCOUNT",  # jimmy 在所有持仓中加入账号名以区分是哪个账号的持仓
            "CODE",
            "QTY",
            "CAN SELL QTY",
            "NOMINAL PRICE",
            "COST",
            "SIDE",
            "TODAY'S PL",
            "PL",
            "TODAY BUY QTY",
            "TODAY SELL QTY",
            "TODAY B&S QTY",
        ],
        "CN": [
            "账户",
            "代码",
            "数量",
            "可卖数量",
            "市价",
            "摊薄成本价",
            "持仓方向",
            "今日盈亏",
            "总盈亏",
            "今日买入总量",
            "今日卖出总量",
            "今日买卖总量",
        ],
    }
    table_columns_total = {
        "EN": ["UNREALIZED PL", "REALIZED PL"],
        "CN": ["未实现盈亏", "已实现盈亏"],
    }
    total_asset = {"EN": "Total Assets", "CN": "资产净值"}
    cash = {"EN": "Cash", "CN": "现金"}
    market_val = {"EN": "Market Value", "CN": "持仓市值"}


class ODT(object):
    """ORDER DETAILS TEXT"""

    window_title = {"EN": "ORDER DETAILS", "CN": "订单详情"}
    account_list_widget = {"EN": "All Accounts", "CN": "所有账户"}
    msg_accn = {"EN": "Account Not Selected", "CN": "账户未选择"}
    acc = {"EN": "Account", "CN": "账户"}
    order_columns = {
        "EN": [
            "Account",
            "Code",
            "Side",
            "Order Type",
            "Price",
            "Qty",
            "Dealt Qty",
            "Dealt Avg Price",
            "Order Status",
            "Time In Force",
            "Market Session",
            "Create Time",
            "Aux Price",
            "Order Id",
        ],
        "CN": [
            "账户",
            "代码",
            "交易方向",
            "订单类型",
            "价格",
            "数量",
            "成交数量",
            "成交均价",
            "订单状态",
            "生效时间",
            "交易时段",
            "创建时间",
            "触发价格",
            "订单Id",
        ],
    }
    deal_columns = {
        "EN": [
            "Account",
            "Code",
            "Trd_side",
            "Price",
            "Qty",
            "Time",
            "Status",
            "Order ID",
        ],
        "CN": [
            "账户",
            "代码",
            "方向",
            "价格",
            "数量",
            "时间",
            "状态",
            "订单ID",
        ],
    }
    choose_account = {"EN": "Double Click to Choose An Account", "CN": "双击选择一个账户"}
    CM = {"EN": "Double Click to Cancel or Modify Order", "CN": "双击取消或修改订单"}
    tab_OT = {"EN": "Today's Orders", "CN": "今日订单"}
    tab_OH = {"EN": "History Orders", "CN": "历史订单"}
    tab_OA = {"EN": "Active Orders", "CN": "活跃订单"}
    tab_DT = {"EN": "Today's Deals", "CN": "今日成交"}
    tab_DH = {"EN": "History Deals", "CN": "历史成交"}
    group_filter = {"EN": "History Filter", "CN": "订单筛选器"}


class CMT(object):
    """CANCEL OR MODIFY ORDER TEXT"""

    window_title = {"EN": "CANCEL/MODIFY ORDER", "CN": "取消/修改订单"}
    text = {"EN": "Please select to cancel or modify order", "CN": "请选择取消或修改订单"}
    button_cancel = {"EN": "Cancel Order", "CN": "取消订单"}
    button_modify = {"EN": "Modify Order", "CN": "修改订单"}
    button_discard = {"EN": "Discard", "CN": "忽略"}
    confirm = {
        "EN": ["Please Confirm", "Do you want to cancel this order?"],
        "CN": ["请确认", "请确认取消该订单"],
    }
