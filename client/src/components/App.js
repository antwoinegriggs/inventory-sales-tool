import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import Inventory from "../pages/Inventory";
import SalesOrders from "../pages/Customer";
import NewProduct from "../pages/NewProduct";
import CustomerList from "../pages/Customer";
import NewCustomer from "../pages/NewCustomer";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // auto-login
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  if (!user) return <Login onLogin={setUser} />;

  return (
    <>
      <Router>
        <NavBar user={user} setUser={setUser} />
        <main>
          <Switch>
            <Route path="/inventory">
              <Inventory user={user} />
            </Route>
            <Route path="/newproduct">
              <NewProduct user={user} />
            </Route>
            <Route path="/sales">
              <SalesOrders />
            </Route>
            <Route path="/customers">
              <CustomerList />
            </Route>
            <Route path="/newcustomer">
              <NewCustomer />
            </Route>
          </Switch>
        </main>
      </Router>
    </>
  );
}

export default App;
