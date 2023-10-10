import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [editedProduct, setEditedProduct] = useState({});

  useEffect(() => {
    fetch("/product_inventory")
      .then((r) => r.json())
      .then(setInventory);
  }, []);

  const handleDelete = (productId) => {
    fetch(`/product_inventory/${productId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.status === 204) {
          setInventory((prevInventory) =>
            prevInventory.filter((product) => product.id !== productId)
          );
        } else {
          console.error("Failed to delete the product.");
        }
      })
      .catch((error) => {
        console.error("Error deleting the product:", error);
      });
  };

  const handleEdit = (product) => {
    setEditedProduct({ ...product });
  };

  const handleUpdate = () => {
    fetch(`/product_inventory/${editedProduct.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editedProduct),
    })
      .then((response) => {
        if (response.status === 200) {
          setInventory((prevInventory) =>
            prevInventory.map((product) =>
              product.id === editedProduct.id ? editedProduct : product
            )
          );
          setEditedProduct({});
        } else {
          console.error("Failed to update the product.");
        }
      })
      .catch((error) => {
        console.error("Error updating the product:", error);
      });
  };

  return (
    <div>
      {inventory.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Product Number</th>
              <th>Product Quantity</th>
              <th>Product Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map((product) => (
              <tr key={product.id}>
                <td>
                  {editedProduct.id === product.id ? (
                    <input
                      type="text"
                      value={editedProduct.product_name}
                      onChange={(e) =>
                        setEditedProduct({
                          ...editedProduct,
                          product_name: e.target.value,
                        })
                      }
                    />
                  ) : (
                    product.product_name
                  )}
                </td>
                <td>{product.product_number}</td>
                <td>
                  {editedProduct.id === product.id ? (
                    <input
                      type="number"
                      value={editedProduct.product_quantity}
                      onChange={(e) =>
                        setEditedProduct({
                          ...editedProduct,
                          product_quantity: e.target.value,
                        })
                      }
                    />
                  ) : (
                    product.product_quantity
                  )}
                </td>
                <td>
                  {editedProduct.id === product.id ? (
                    <input
                      type="number"
                      value={editedProduct.product_price}
                      onChange={(e) =>
                        setEditedProduct({
                          ...editedProduct,
                          product_price: e.target.value,
                        })
                      }
                    />
                  ) : (
                    product.product_price
                  )}
                </td>
                <td>
                  {editedProduct.id === product.id ? (
                    <>
                      <button onClick={handleUpdate}>Save</button>
                      <button onClick={() => setEditedProduct({})}>
                        Cancel
                      </button>
                    </>
                  ) : (
                    <>
                      <button onClick={() => handleEdit(product)}>Edit</button>
                      <button onClick={() => handleDelete(product.id)}>
                        Delete
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <>
          <h2>No Inventory Found</h2>
          <button>
            <Link to="/newproduct">Add New Product</Link>
          </button>
        </>
      )}
    </div>
  );
}

export default Inventory;
