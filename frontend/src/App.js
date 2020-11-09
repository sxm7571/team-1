import React, { useState, useEffect } from "react";
import axios from 'axios';
import jwt_decode from "jwt-decode";
import { Switch, Route, Link, BrowserRouter as Router } from "react-router-dom";
import './App.css';

import Context from "./contexts/productContext";
import AddProduct from './components/addProduct';
import Cart from './components/cart';
import Login from './components/login';
import ProductList from './components/productList';

const App = (props) => {
  const [user, setUser] = useState(null);
  const [cart, setCart] = useState({});
  const [products, setProducts] = useState([]);
  const [showMenu, setShowMenu] = useState(false);
  const routerRef = React.createRef();

  useEffect(() => {
    let user = localStorage.getItem("user");
    user = user ? JSON.parse(user) : null;
    setUser(user);
  }, [])

  const login = async (email, password) => {
    const res = await axios.post(
        'http://localhost:3001/login',
        { email, password },
    ).catch((res) => {
      return { status: 401, message: 'Unauthorized' }
    })

    if(res.status === 200) {
      const { email } = jwt_decode(res.data.accessToken)
      const user = {
        email,
        token: res.data.accessToken,
        accessLevel: email === 'admin@example.com' ? 0 : 1
      }

      setUser(user);
      localStorage.setItem("user", JSON.stringify(user));
      return true;
    } else {
      return false;
    }
  }

  const logout = e => {
    e.preventDefault();
    setUser(null)
    setCart({})
    setProducts([])
    localStorage.removeItem("user");
  };

  return (
      <Context.Provider
          value={{
            user,
            cart,
            products,
            //removeFromCart: removeFromCart,
            //addToCart: addToCart,
            login,
            //addProduct: addProduct,
            //clearCart: clearCart,
            //checkout: checkout
          }}
      >
        <Router ref={routerRef}>
          <div className="App">
            <nav
                className="navbar container"
                role="navigation"
                aria-label="main navigation"
            >
              <div className="navbar-brand">
                <b className="navbar-item is-size-4 site-header ">Personalized ecommerce</b>
                <label
                    role="button"
                    class="navbar-burger burger"
                    aria-label="menu"
                    aria-expanded="false"
                    data-target="navbarBasicExample"
                    onClick={e => {
                      e.preventDefault();
                      setShowMenu(!showMenu)
                    }}
                >
                  <span aria-hidden="true"></span>
                  <span aria-hidden="true"></span>
                  <span aria-hidden="true"></span>
                </label>
              </div>
              <div className={`navbar-menu ${
                  showMenu ? "is-active" : ""
              }`}>
                <Link to="/products" className="navbar-item">
                  Products
                </Link>
                {user && user.accessLevel < 1 && (
                    <Link to="/add-product" className="navbar-item">
                      Add Product
                    </Link>
                )}
                <Link to="/cart" className="navbar-item">
                  Cart
                  <span
                      className="tag is-primary"
                      style={{ marginLeft: "5px" }}
                  >
                    { Object.keys(cart).length }
                  </span>
                </Link>
                {!user ? (
                    <Link to="/login" className="navbar-item">
                      Login
                    </Link>
                ) : (
                    <Link to="/" onClick={logout} className="navbar-item">
                      Logout
                    </Link>
                )}
              </div>
            </nav>
            <Switch>
              <Route exact path="/" component={ProductList} />
              <Route exact path="/login" component={Login} />
              <Route exact path="/cart" component={Cart} />
              <Route exact path="/add-product" component={AddProduct} />
              <Route exact path="/products" component={ProductList} />
            </Switch>
          </div>
        </Router>
      </Context.Provider>
  );
}

export default App;
