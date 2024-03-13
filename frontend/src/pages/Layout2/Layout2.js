import React from "react";
import { Link } from "react-router-dom";
import { ReactComponent as Logo } from '../../assets/apollo-logo-black.svg';

import "../Layout/Layout.css"

function Layout2() {
    return(
        <div className="container">
            <Logo className="logo" />
            <Link to="/"><h1>Apenas um teste aqui sry!</h1></Link>
        </div>
    )
}

export default Layout2
