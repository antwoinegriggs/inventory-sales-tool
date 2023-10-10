import { useEffect, useState } from "react";
import { useHistory } from "react-router";
// import ReactMarkdown from "react-markdown";

function NewProduct({ user }) {
  const [product_name, setProductName] = useState([]);
  const [product_number, setProductNum] = useState([]);
  const [product_quantity, setProductQuant] = useState([]);
  const [product_price, setProductPrice] = useState([]);

  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();

  function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);
    fetch("/product_inventory", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_name,
        product_number,
        product_quantity,
        product_price,
      }),
    }).then((r) => {
      setIsLoading(false);
      if (r.ok) {
        history.push("/");
      } else {
        r.json().then((err) => setErrors(err.errors));
      }
    });
  }

  return (
    <div>
      <div>
        <h2>Create Product</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="title">Product Name: </label>
            <input
              type="text"
              id="name"
              value={product_name}
              onChange={(e) => setProductName(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="product_number">Product Number: </label>
            <input
              type="text"
              id="product_number"
              value={product_number}
              onChange={(e) => setProductNum(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="quantity">Quantity: </label>
            <input
              type="text"
              id="quantity"
              value={product_quantity}
              onChange={(e) => setProductQuant(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="title">Product Price: </label>
            <input
              type="text"
              id="price"
              value={product_price}
              onChange={(e) => setProductPrice(e.target.value)}
            />
          </div>
          <div>
            <button color="primary" type="submit">
              {isLoading ? "Loading..." : "Submit"}
            </button>
          </div>
          <div>
            {errors.map((err) => (
              <error key={err}>{err}</error>
            ))}
          </div>
        </form>
      </div>
    </div>
  );
}

export default NewProduct;
