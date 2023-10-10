import React, { useState } from "react";
import { useHistory } from "react-router";

function NewCustomer({ user }) {
  const [name, setName] = useState("");
  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();

  function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);
    fetch("/customers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
      }),
    })
      .then((r) => {
        setIsLoading(false);
        if (r.ok) {
          history.push("/");
        } else {
          r.json().then((err) => setErrors(err.errors));
        }
      })
      .catch((error) => {
        console.error("Error adding customer:", error);
        setIsLoading(false);
      });
  }

  return (
    <div>
      <div>
        <h2>Create Customer</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="name">Customer Name: </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div>
            <button type="submit">{isLoading ? "Loading..." : "Submit"}</button>
          </div>
          <div>
            {errors && errors.length > 0
              ? errors.map((err, index) => (
                  <div key={index} className="error">
                    {err}
                  </div>
                ))
              : null}
          </div>
        </form>
      </div>
    </div>
  );
}

export default NewCustomer;
