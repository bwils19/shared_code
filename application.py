import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # Display current portfolio

    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
    stocks = db.execute("SELECT * FROM portfolio WHERE username = :username", username=username)
    total_sum = []

    for s in stocks:

        symbol = str(s["Symbol"])
        name = lookup(symbol)["name"]

        price = lookup(symbol)["price"]
        shares = int(s["Shares"])
        total = shares * price

        s["name"] = name
        s["price"] = usd(price)
        s["total"] = usd(total)
        s["symbol"] = symbol
        s["shares"] = shares
        total_sum.append(float(total))


    cash_available = db.execute("SELECT cash FROM users WHERE username = :username", username = username)[0]["cash"]
    cash_tot = sum(total_sum) + cash_available

    return render_template("index.html", stocks = stocks, cash_available = usd(cash_available), cash_total = usd(cash_tot))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # get all information for the requested stock symbol
        req = lookup(request.form.get("symbol"))

        share = request.form.get("shares")
        share = int(share)

        if req == None:
            return apology("Missing Symbol", 400)

        # Ensure input is a postive integer
        if not isinstance(share, int) or share < 1:
            return apology("Please provide valid share amount", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=int(session['user_id']))

        # determine value of request
        value = req["price"] * share

        stock_owned = db.execute("select * from portfolio WHERE username = :username AND Symbol = :symbol",
                            username=db.execute("SELECT username FROM users WHERE id = :uid",
                            uid=int(session['user_id']))[0]["username"], symbol=req['symbol'])
        print(stock_owned)

        # check if user has enough to buy the requested amount of particular stock
        if int(cash[0]["cash"]) < value:
            return apology("You do not have enough cash to buy this stock", 403)

        # if the user has enough dough for the purchase
        else:

            # subtract the cost of the transaction from the user's cash amount
            db.execute("UPDATE users SET cash = cash - :value WHERE id = :uid", value=value, uid=int(session['user_id']))

            # get a timestamp of the transaction
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # insert the transaction into the history table
            db.execute("INSERT INTO history (username, symbol, price, shares, timestamp, action) VALUES (:username, :symbol, :price, :share, :timestamp, 'BUY')",
            username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"],
            symbol=req['symbol'], price=req['price'], share=request.form.get('shares'), timestamp = timestamp)

            # if the user already owns some of the stock, add current purchase
            if len(stock_owned) == 1:
                new_share_amt = int(stock_owned[0]["Shares"]) + share
                new_total = float(stock_owned[0]["Total"]) + value

                db.execute("UPDATE portfolio SET shares = :share, total = :total WHERE symbol = :symbol and username = :username",
                username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"],
                symbol=req['symbol'], share=new_share_amt, total = new_total)


            # If this stock is not already owned by user, create a new row
            else:
                db.execute("INSERT INTO portfolio (username, symbol, shares, total) VALUES (:username, :symbol, :share, :total)",
                username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"],
                symbol=req['symbol'], share=request.form.get('shares'), total = (req["price"]*share))

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    trans = db.execute("SELECT symbol, price, shares, timestamp, action FROM history WHERE username = :username",
                username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"])

    for t in trans:
        symbol = str(t["symbol"])
        name = lookup(symbol)["name"]
        t["name"] = name

    return render_template("history.html", trans=trans)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # store the results from the requested quote
        req = lookup(request.form.get("symbol"))

        if req == None:
            return apology("invalid symbol", 400)

        # return the results of the search
        else:
            return render_template("quoted.html", name = req["name"], symbol = req["symbol"],
                    price = usd(req["price"]), high = req["week52High"], low = req["week52Low"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # if a username was not provided
        if not request.form.get("username"):
            return apology("please provide a username")

        # be sure user supplied a password
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("please provide a password")

        # make sure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # get a list of usernames already registerd
        user_list = db.execute("SELECT DISTINCT(username) FROM users")

        if request.form.get("password") in user_list:
            return apology("That username is not available. Please choose a new one.")

        # save user
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        if not result:
            return apology("username is not available, please provide a different username")

        session["user_id"] = result

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stocks = db.execute("SELECT DISTINCT Symbol FROM portfolio WHERE username = :username",
        username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"])

    stock_list = []
    for i in range(len(stocks)):
        stock_list.append(stocks[i]['Symbol'])

    if request.method == "POST":

        stock = request.form.get("symbol")
        print(stock)
        share = request.form.get("shares")
        share = int(share)

        if stock == None:
            return apology("Missing Symbol", 400)

        # Ensure input is a postive integer
        elif not isinstance(share, int) or share < 1:
            return apology("Please provide valid share amount", 400)

        shares_owned = db.execute("select Shares, Total from portfolio WHERE username = :username and Symbol = :symbol",
                                    username=db.execute("SELECT username FROM users WHERE id = :uid",
                                    uid=int(session['user_id']))[0]["username"], symbol=stock)

        print(f'Shares owned {shares_owned}')

        if share > int(shares_owned[0]["Shares"]):
            return apology("You do not own enough shares to sell the requested amount", 400)

        else:

            # determine value of request
            req = lookup(stock)
            value = req["price"] * share
            print(f"value {value}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # insert the transaction into the history table
            db.execute("INSERT INTO history (username, symbol, price, shares, timestamp, action) VALUES (:username, :symbol, :price, :share, :timestamp, 'SELL')",
                        username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"],
                        symbol=stock, price=req['price'], share=share, timestamp = timestamp)

            if share == shares_owned[0]["Shares"]:
                db.execute("DELETE FROM portfolio WHERE username = :username AND symbol = :symbol",
                            username=db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"],
                            symbol=stock)

            else:
                new_share_amt = int(shares_owned[0]["Shares"]) - share
                new_total = new_share_amt * req["price"]
                db.execute("UPDATE portfolio SET Shares = :shares, Total = :total WHERE username = :username and Symbol = :symbol",
                    username=db.execute("SELECT username FROM users WHERE id = :uid",
                    uid=int(session['user_id']))[0]["username"], symbol=stock, shares=new_share_amt, total=new_total)

            # add the selling amount of the transaction to the user's cash amount
            db.execute("UPDATE users SET cash = cash + :value WHERE id = :uid", value=new_total, uid=int(session['user_id']))

        return redirect("/")

    else:
        return render_template("sell.html", stocks=stock_list)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
