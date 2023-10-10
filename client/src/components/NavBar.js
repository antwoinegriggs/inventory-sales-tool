import React from "react";
import { Link } from "react-router-dom";

function NavBar({ user, setUser }) {
  function handleLogoutClick() {
    fetch("/logout", { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setUser(null);
      }
    });
  }

  return (
    <div>
      <h2>
        <Link to="/">IST</Link>
      </h2>
      <nav>
        <button>
          <Link to="/inventory">Inventory</Link>
        </button>
        <button>
          <Link to="/newproduct">New Product</Link>
        </button>
        <button>
          <Link to="/customers">Customers</Link>
        </button>
        <button>
          <Link to="/newcustomer">New Customer</Link>
        </button>
        <button variant="outline" onClick={handleLogoutClick}>
          Logout
        </button>
      </nav>
    </div>
  );
}

export default NavBar;
