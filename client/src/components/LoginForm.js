import React, { useState } from "react";

function handleSubmit(e) {
  e.preventDefault();
  setIsLoading(true);
  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  }).then((r) => {
    setIsLoading(false);
    if (r.ok) {
      r.json().then((user) => onLogin(user));
    } else {
      r.json().then((err) => setErrors(err.errors));
    }
  });
}

return <></>;
